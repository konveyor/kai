import asyncio
import functools
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, TypeVar

from langchain.chat_models import init_chat_model
from langchain_community.chat_models.fake import FakeListChatModel
from langchain_core.language_models.chat_models import BaseChatModel
from sqlalchemy.exc import DBAPIError, IntegrityError, OperationalError
from sqlalchemy.exc import TimeoutError as SQLAlchemyTimeoutError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from kai_mcp_solution_server.constants import log
from kai_mcp_solution_server.db.dao import get_async_engine, kill_idle_connections
from kai_mcp_solution_server.settings import SolutionServerSettings

P = ParamSpec("P")
T = TypeVar("T")


class _SharedResources:
    """Global shared resources initialized once at module level."""

    engine: AsyncEngine | None = None
    session_maker: async_sessionmaker[AsyncSession] | None = None
    model: BaseChatModel | None = None
    initialization_lock: asyncio.Lock | None = None
    initialized: bool = False
    # Semaphore to limit concurrent DB operations (prevent connection pool exhaustion)
    db_semaphore: asyncio.Semaphore | None = None
    max_concurrent_ops: int = 80  # Allow up to 80 concurrent DB operations


async def _initialize_shared_resources() -> None:
    """Initialize shared resources once, protected by a lock."""
    if _SharedResources.initialization_lock is None:
        _SharedResources.initialization_lock = asyncio.Lock()

    async with _SharedResources.initialization_lock:
        if _SharedResources.initialized:
            return

        from kai_mcp_solution_server.db.dao import Base

        log(
            "Initializing shared database engine and model (once for all connections)..."
        )
        settings = SolutionServerSettings()

        # Initialize semaphore to limit concurrent DB operations
        _SharedResources.db_semaphore = asyncio.Semaphore(
            _SharedResources.max_concurrent_ops
        )
        log(
            f"DB operation semaphore initialized with limit: {_SharedResources.max_concurrent_ops}"
        )

        # Initialize database engine
        _SharedResources.engine = await get_async_engine(settings.db_dsn)
        async with _SharedResources.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        _SharedResources.session_maker = async_sessionmaker(
            bind=_SharedResources.engine, expire_on_commit=False
        )

        # Initialize model
        if settings.llm_params is None:
            raise ValueError("LLM parameters must be provided in the settings.")
        elif settings.llm_params.get("model") == "fake":
            llm_params = settings.llm_params.copy()
            llm_params.pop("model", None)
            if "responses" not in llm_params:
                llm_params["responses"] = ["fake response"]
            _SharedResources.model = FakeListChatModel(**llm_params)
        else:
            _SharedResources.model = init_chat_model(**settings.llm_params)

        _SharedResources.initialized = True
        log("Shared resources initialized successfully")


async def _recover_from_db_error() -> None:
    """Recover from database errors by killing idle connections or recreating engine."""
    if _SharedResources.engine is not None:
        log("Recovering from database error - killing idle connections...")
        try:
            await kill_idle_connections(_SharedResources.engine)
            log("Successfully killed idle connections")
        except Exception as e:
            log(f"Failed to kill idle connections: {e}")
            log("Disposing and recreating engine...")
            await _SharedResources.engine.dispose()
            _SharedResources.initialized = False
            await _initialize_shared_resources()


class KaiSolutionServerContext:
    """Per-connection context that references shared resources."""

    def __init__(self, settings: SolutionServerSettings) -> None:
        self.settings = settings
        self.lock = asyncio.Lock()
        # References to shared resources (set in create())
        self.engine: AsyncEngine | None = None
        self.session_maker: async_sessionmaker[AsyncSession] | None = None
        self.model: BaseChatModel | None = None

    async def create(self) -> None:
        """Initialize shared resources if needed and reference them."""
        await _initialize_shared_resources()

        if _SharedResources.engine is None:
            raise RuntimeError("Database engine failed to initialize")
        if _SharedResources.session_maker is None:
            raise RuntimeError("Session maker failed to initialize")
        if _SharedResources.model is None:
            raise RuntimeError("Model failed to initialize")

        log(f"Connection using shared engine: {id(_SharedResources.engine)}")
        self.engine = _SharedResources.engine
        self.session_maker = _SharedResources.session_maker
        self.model = _SharedResources.model


def with_db_recovery(
    func: Callable[..., Coroutine[Any, Any, T]],
) -> Callable[..., Coroutine[Any, Any, T]]:
    """Decorator to execute database operations with automatic recovery on connection errors.

    Uses a semaphore to limit concurrent DB operations and prevent pool exhaustion.
    Implements exponential backoff with retry on connection errors.
    """

    @functools.wraps(func)
    async def wrapper(
        kai_ctx: KaiSolutionServerContext, *args: Any, **kwargs: Any
    ) -> T:
        if _SharedResources.db_semaphore is None:
            raise RuntimeError("Database semaphore not initialized")
        if kai_ctx.session_maker is None:
            raise RuntimeError("Session maker not initialized")

        # Semaphore ensures we don't overwhelm the connection pool
        async with _SharedResources.db_semaphore:
            max_retries = 3
            base_delay = 0.1  # 100ms base delay

            for attempt in range(max_retries):
                try:
                    return await func(kai_ctx, *args, **kwargs)
                except IntegrityError:
                    raise
                except SQLAlchemyTimeoutError:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2**attempt)  # Exponential backoff
                        log(
                            f"Connection pool timeout (attempt {attempt + 1}), retrying in {delay}s..."
                        )
                        await asyncio.sleep(delay)
                        await _recover_from_db_error()
                    else:
                        log(f"Connection pool exhausted after {max_retries} attempts")
                        raise
                except (DBAPIError, OperationalError) as e:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2**attempt)
                        log(
                            f"Database error (attempt {attempt + 1}): {e}, retrying in {delay}s..."
                        )
                        await asyncio.sleep(delay)
                        await _recover_from_db_error()
                        await kai_ctx.create()
                    else:
                        log(f"Database error after {max_retries} attempts, giving up")
                        raise

            # This should never be reached due to the loop structure,
            # but mypy needs an explicit unreachable marker
            raise RuntimeError("Unexpected: retry loop completed without returning")

    return wrapper
