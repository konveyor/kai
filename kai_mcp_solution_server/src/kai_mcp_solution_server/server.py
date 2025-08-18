import asyncio
import json
import os
import sys
import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, Any, cast

from fastmcp import Context, FastMCP
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel
from langchain_community.chat_models.fake import FakeListChatModel
from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict
from sqlalchemy import URL, and_, make_url, or_, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.ast_diff.parser import Language, extract_ast_info
from kai_mcp_solution_server.constants import log, logger
from kai_mcp_solution_server.db.dao import (
    DBFile,
    DBHint,
    DBIncident,
    DBSolution,
    DBViolation,
    get_async_engine,
)
from kai_mcp_solution_server.db.python_objects import (
    SolutionFile,
    SolutionStatus,
    ViolationID,
    associate_files,
    get_diff,
)


class SolutionServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kai_")

    db_dsn: Annotated[URL, NoDecode]
    """
    Example DSNs:
    - PostgreSQL: `postgresql+asyncpg://username:password@host:port/database`
    - SQLite: `sqlite+aiosqlite:///path/to/database.db`
    """

    llm_params: dict[str, Any] | None

    drop_all: bool = False

    @model_validator(mode="before")
    @classmethod
    def validate_db_dsn(cls, data: Any) -> Any:
        """
        Environment variables added:
        - `KAI_DB_DRIVERNAME`
        - `KAI_DB_USERNAME`
        - `KAI_DB_PASSWORD`
        - `KAI_DB_HOST`
        - `KAI_DB_PORT`
        - `KAI_DB_DATABASE`

        1. Any parameters supplied via Python's `SolutionServerSettings`
           constructor takes highest precedence, then any configuration supplied
           via `KAI_DB_DSN`.
        2. Try to parse `KAI_DB_DSN` as a json object, containing `drivername`,
           `username`, etc... If that fails, parse it as a connection string.
        3. If the `KAI_DB_DSN` environment variable or the `db_dsn` field is not
           supplied, try to get all information from the new variables
        """

        if isinstance(data, dict):
            kwargs: dict[str, Any]

            if "db_dsn" not in data:
                kwargs = {}

            elif isinstance(data["db_dsn"], URL):
                kwargs = data["db_dsn"]._asdict()

            elif isinstance(data["db_dsn"], dict):
                kwargs = data["db_dsn"]

            elif isinstance(data["db_dsn"], str):
                try:
                    kwargs = json.loads(data["db_dsn"])
                except json.JSONDecodeError:
                    kwargs = make_url(data["db_dsn"])._asdict()

            else:
                raise ValueError(
                    f"Invalid type for db_dsn: {type(data['db_dsn'])}. Expected missing, str, dict, or URL."
                )

            for key in [
                "drivername",
                "username",
                "password",
                "host",
                "port",
                "database",
            ]:
                if kwargs.get(key) is None:
                    kwargs[key] = os.getenv(f"KAI_DB_{key.upper()}", None)

            data["db_dsn"] = URL.create(**kwargs)

        return data


class KaiSolutionServerContext:
    def __init__(self, settings: SolutionServerSettings) -> None:
        self.settings = settings
        self.lock = asyncio.Lock()

    async def create(self) -> None:
        logger.info("[STARTUP] Initializing database engine...")
        self.engine = await get_async_engine(
            self.settings.db_dsn, self.settings.drop_all
        )
        self.session_maker = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )
        logger.info("[STARTUP] Database engine initialized successfully")

        self.model: BaseChatModel

        if self.settings.llm_params is None:
            logger.error("[STARTUP_ERROR] LLM parameters not provided")
            raise ValueError("LLM parameters must be provided in the settings.")
        elif self.settings.llm_params.get("model") == "fake":
            logger.info("[STARTUP] Using fake LLM model for testing")
            llm_params = self.settings.llm_params.copy()
            llm_params.pop("model", None)
            if "responses" not in llm_params:
                llm_params["responses"] = [
                    "fake response",
                ]
            self.model = FakeListChatModel(**llm_params)
        else:
            model_name = self.settings.llm_params.get("model", "unknown")
            logger.info(f"[STARTUP] Initializing LLM model: {model_name}")
            self.model = init_chat_model(**self.settings.llm_params)

        logger.info("[STARTUP] LLM model initialized successfully")


@asynccontextmanager
async def kai_solution_server_lifespan(
    server: FastMCP[KaiSolutionServerContext],
) -> AsyncIterator[KaiSolutionServerContext]:
    log("kai_solution_server_lifespan")
    logger.info("[STARTUP] KAI MCP Solution Server starting...")
    try:
        settings = SolutionServerSettings()
        log(f"Settings: {settings.model_dump_json(indent=2)}")
        logger.info(
            f"[STARTUP] Database DSN: {settings.db_dsn.render_as_string(hide_password=True)}"
        )
        logger.info(f"[STARTUP] Drop all tables: {settings.drop_all}")

        log("creating context")
        logger.info("[STARTUP] Creating server context...")
        ctx = KaiSolutionServerContext(settings)
        await ctx.create()
        log("yielding context")
        logger.info("[STARTUP] Server context created successfully")
        logger.info("[STARTUP] KAI MCP Solution Server ready to accept requests")

        yield ctx
    except Exception as e:
        logger.error(f"[STARTUP_ERROR] Failed to start server: {str(e)}")
        log(f"Error in lifespan: {traceback.format_exc()}")
        raise e
    finally:
        logger.info("[SHUTDOWN] KAI MCP Solution Server shutting down")


mcp: FastMCP[KaiSolutionServerContext] = FastMCP(
    "KaiSolutionServer", lifespan=kai_solution_server_lifespan, dependencies=[]
)


class CreateIncidentResult(BaseModel):
    incident_id: int
    solution_id: int


async def create_incident(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    extended_incident: ExtendedIncident,
) -> int:
    async with kai_ctx.session_maker.begin() as session:
        violation_stmt = select(DBViolation).where(
            DBViolation.ruleset_name == extended_incident.ruleset_name,
            DBViolation.violation_name == extended_incident.violation_name,
        )

        violation = (await session.execute(violation_stmt)).scalar_one_or_none()
        if violation is None:
            log(
                f"Violation {extended_incident.ruleset_name} - {extended_incident.violation_name} not found in the database.",
            )
            logger.info(
                f"[DB_STATE] Creating new violation: {extended_incident.ruleset_name}/{extended_incident.violation_name}"
            )

            violation = DBViolation(
                ruleset_name=extended_incident.ruleset_name,
                ruleset_description=extended_incident.ruleset_description,
                violation_name=extended_incident.violation_name,
                violation_category=extended_incident.violation_category,
                incidents=set(),
                hints=set(),
            )
            session.add(violation)
        else:
            logger.debug(
                f"[DB_STATE] Using existing violation: {extended_incident.ruleset_name}/{extended_incident.violation_name}"
            )

        incident = DBIncident(
            client_id=client_id,
            uri=extended_incident.uri,
            message=extended_incident.message,
            code_snip=extended_incident.code_snip,
            line_number=extended_incident.line_number,
            variables=extended_incident.variables,
            violation=violation,
            solution=None,
        )
        session.add(incident)
        logger.info(
            f"[DB_STATE] Creating incident for client {client_id} at {extended_incident.uri}:{extended_incident.line_number}"
        )

        await session.commit()
        logger.info(f"[DB_STATE] Incident committed with ID: {incident.id}")

    return incident.id


@mcp.tool(name="create_incident")
async def tool_create_incident(
    ctx: Context,
    client_id: str,
    extended_incident: ExtendedIncident,
) -> int:
    """
    Create an incident in the database.
    This function will create a new incident in the database, associating it with
    the provided client ID and the extended incident data. If the violation
    associated with the incident does not exist in the database, it will be created
    as well.
    """
    logger.info(
        f"[REQUEST] create_incident - client_id: {client_id}, violation: {extended_incident.ruleset_name}/{extended_incident.violation_name}, uri: {extended_incident.uri}"
    )
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        result = await create_incident(
            kai_ctx,
            client_id,
            extended_incident,
        )
        logger.info(f"[RESPONSE] create_incident - Created incident with ID: {result}")
        return result


@mcp.tool(name="create_multiple_incidents")
async def tool_create_multiple_incidents(
    ctx: Context,
    client_id: str,
    extended_incidents: list[ExtendedIncident],
) -> list[CreateIncidentResult]:
    """
    Create multiple incidents in the database.
    This function will create multiple new incidents in the database, associating
    them with the provided client ID and the list of extended incident data.
    If any of the violations associated with the incidents do not exist in the
    database, they will be created as well.
    """
    logger.info(
        f"[REQUEST] create_multiple_incidents - client_id: {client_id}, count: {len(extended_incidents)}"
    )
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    results: list[CreateIncidentResult] = []

    async with kai_ctx.lock:
        for i, extended_incident in enumerate(extended_incidents):
            logger.debug(
                f"  Creating incident {i+1}/{len(extended_incidents)}: {extended_incident.ruleset_name}/{extended_incident.violation_name}"
            )
            incident_id = await create_incident(kai_ctx, client_id, extended_incident)
            results.append(CreateIncidentResult(incident_id=incident_id, solution_id=0))

    logger.info(
        f"[RESPONSE] create_multiple_incidents - Created {len(results)} incidents"
    )
    return results


async def create_solution(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    incident_ids: list[int],
    before: list[SolutionFile],
    after: list[SolutionFile],
    reasoning: str | None = None,
    used_hint_ids: list[int] | None = None,
) -> int:
    if len(incident_ids) == 0:
        logger.error(
            f"[DB_STATE] create_solution called with no incident IDs for client {client_id}"
        )
        raise ValueError("At least one incident ID must be provided.")

    if used_hint_ids is None:
        used_hint_ids = []

    logger.info(
        f"[DB_STATE] Creating solution for client {client_id} with {len(incident_ids)} incidents"
    )

    async with kai_ctx.session_maker.begin() as session:
        incident_ids_cond = [
            and_(DBIncident.id == incident_id, DBIncident.client_id == client_id)
            for incident_id in incident_ids
        ]
        incidents_stmt = select(DBIncident).where(or_(*incident_ids_cond))
        incidents = (await session.execute(incidents_stmt)).scalars().all()

        hint_stmt = select(DBHint).where(DBHint.id.in_(used_hint_ids))
        hints = (await session.execute(hint_stmt)).scalars().all()

        if missing_ids := set(used_hint_ids) - {hint.id for hint in hints}:
            raise ValueError(
                f"Some hint IDs {missing_ids} do not exist in the database."
            )

        # Try to match the before files. If you can't, create them.
        # Create the after files. Associate them with the before files.
        # Create the solution.

        db_before_files: set[DBFile] = set()
        for file in before:
            stmt = (
                select(DBFile)
                .where(
                    DBFile.client_id == client_id,
                    DBFile.uri == file.uri,
                )
                .order_by(DBFile.created_at.desc())
            )
            prev_before = (await session.execute(stmt)).scalars().first()

            if prev_before is None or prev_before.content != file.content:
                next_before = DBFile(
                    client_id=client_id,
                    uri=file.uri,
                    content=file.content,
                    status=SolutionStatus.PENDING,
                    solution_before=set(),
                    solution_after=set(),
                )
                session.add(next_before)
                db_before_files.add(next_before)
            else:
                db_before_files.add(prev_before)

        db_after_files: set[DBFile] = set()
        for file in after:
            # FIXME: Something is fishy here...
            next_after = DBFile(
                client_id=client_id,
                uri=file.uri,
                content=file.content,
                status=SolutionStatus.PENDING,
                solution_before=set(),
                solution_after=set(),
            )

            stmt = (
                select(DBFile)
                .where(
                    DBFile.client_id == client_id,
                    DBFile.uri == file.uri,
                )
                .order_by(DBFile.created_at.desc())
            )

            db_after_files.add(next_after)
            session.add(next_after)

        solution = DBSolution(
            client_id=client_id,
            before=db_before_files,
            after=db_after_files,
            reasoning=reasoning,
            solution_status=SolutionStatus.UNKNOWN,
            incidents=set(incidents),
            hints=set(hints),
        )

        logger.info(
            f"[DB_STATE] Solution created with status: {solution.solution_status}, before_files: {len(db_before_files)}, after_files: {len(db_after_files)}"
        )

        session.add(solution)
        await session.commit()

        logger.info(
            f"[DB_STATE] Solution committed with ID: {solution.id}, status: {solution.solution_status}"
        )

    return solution.id


@mcp.tool(name="create_solution")
async def tool_create_solution(
    ctx: Context,
    client_id: str,
    incident_ids: list[int],
    before: list[SolutionFile],
    after: list[SolutionFile],
    reasoning: str | None = None,
    used_hint_ids: list[int] | None = None,
) -> int:
    """
    Create a solution in the database.
    This function will create a new solution in the database, associating it with
    the provided client ID, incident IDs, change set, reasoning, and used hint IDs.
    If the incident IDs do not exist in the database, a ValueError will be raised.
    If the used hint IDs do not exist in the database, a ValueError will be raised
    """
    logger.info(
        f"[REQUEST] create_solution - client_id: {client_id}, incidents: {incident_ids}, files_before: {len(before)}, files_after: {len(after)}"
    )
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        result = await create_solution(
            kai_ctx,
            client_id,
            incident_ids,
            before,
            after,
            reasoning,
            used_hint_ids,
        )
        logger.info(f"[RESPONSE] create_solution - Created solution with ID: {result}")
        return result


async def generate_hint_v1(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
) -> None:
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(
            DBSolution.client_id == client_id,
            or_(
                DBSolution.solution_status == SolutionStatus.ACCEPTED,
                DBSolution.solution_status == SolutionStatus.MODIFIED,
            ),
        )
        solutions = (await session.execute(solutions_stmt)).scalars().all()
        if len(solutions) == 0:
            log(
                f"No accepted or modified solutions found for client {client_id}. No hint generated."
            )
            return

        for solution in solutions:
            prompt = (
                "The following incidents had this accepted solution. "
                "Generate a hint for the user so that they can perform the same solution:\n"
            )

            for i, incident in enumerate(solution.incidents):
                prompt += (
                    f"Incident {i + 1}:\n"
                    f"  URI: {incident.uri}\n"
                    f"  Message: {incident.message}\n"
                    f"  Code Snippet: {incident.code_snip}\n"
                    f"  Line Number: {incident.line_number}\n"
                    f"  Variables: {incident.variables}\n"
                    f"  Violation: {incident.violation.ruleset_name} - "
                    f"  {incident.violation.violation_name}\n\n"
                )

            diff = get_diff(
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.before],
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.after],
            )

            prompt += "Solution:\n" f"{diff}\n\n"

            log(f"Generating hint for client {client_id} with prompt:\n{prompt}")

            response = await kai_ctx.model.ainvoke(prompt)

            log(f"Generated hint: {response.content}")

            hint = DBHint(
                text=str(response.content),
                violations=set(
                    incident.violation
                    for incident in solution.incidents
                    if incident.violation is not None
                ),
                solutions=set([solution]),
            )
            session.add(hint)

            await session.flush()

        await session.commit()


async def generate_hint_v2(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
) -> None:
    # print(f"Generating hint for client {client_id}", file=sys.stderr)
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(
            DBSolution.client_id == client_id,
            or_(
                DBSolution.solution_status == SolutionStatus.ACCEPTED,
                DBSolution.solution_status == SolutionStatus.MODIFIED,
            ),
        )
        solutions = (await session.execute(solutions_stmt)).scalars().all()
        if len(solutions) == 0:
            print(
                f"No accepted solutions found for client {client_id}. No hint generated.",
                file=sys.stderr,
            )
            return

        for solution in solutions:
            prompt = (
                "The following incidents had this accepted solution. "
                "Generate a hint for the user so that they can create the same solution:\n"
            )

            for i, incident in enumerate(solution.incidents):
                prompt += (
                    f"Incident {i + 1}:\n"
                    f"  URI: {incident.uri}\n"
                    f"  Message: {incident.message}\n"
                    f"  Code Snippet: {incident.code_snip}\n"
                    f"  Line Number: {incident.line_number}\n"
                    f"  Variables: {incident.variables}\n"
                    f"  Violation: {incident.violation.ruleset_name} - "
                    f"  {incident.violation.violation_name}\n\n"
                )

            diff = associate_files(
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.before],
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.after],
            )

            ast_diffs: list[dict[str, Any]] = []
            for (_before_uri, _after_uri), (before_file, after_file) in diff.items():
                if before_file.content == after_file.content:
                    continue

                ast_diffs.append(
                    extract_ast_info(before_file.content, language=Language.JAVA).diff(
                        extract_ast_info(after_file.content, language=Language.JAVA)
                    )
                )

            ast_diff_str = "\n\n".join(str(a) for a in ast_diffs if a is not None)
            prompt += f"AST Diff:\n{ast_diff_str}\n\n"

            # print(f"Generating hint for client {client_id} with prompt:\n{prompt}", file=sys.stderr)

            response = await kai_ctx.model.ainvoke(prompt)

            # print(f"Generated hint: {response.content}", file=sys.stderr)

            hint = DBHint(
                text=str(response.content),
                violations=set(
                    incident.violation
                    for incident in solution.incidents
                    if incident.violation is not None
                ),
                solutions=set([solution]),
            )
            session.add(hint)

            await session.flush()

        await session.commit()


async def generate_hint_v3(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
) -> None:
    """
    Generate hints for accepted solutions using improved prompt format with better structure.
    """
    logger.info(f"[HINT_GENERATION] Starting hint generation for client {client_id}")
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(
            DBSolution.client_id == client_id,
            or_(
                DBSolution.solution_status == SolutionStatus.ACCEPTED,
                DBSolution.solution_status == SolutionStatus.MODIFIED,
            ),
        )
        solutions = (await session.execute(solutions_stmt)).scalars().all()
        if len(solutions) == 0:
            logger.info(
                f"[HINT_GENERATION] No accepted or modified solutions found for client {client_id}. No hint generated."
            )
            print(
                f"No accepted or modified solutions found for client {client_id}. No hint generated.",
                file=sys.stderr,
            )
            return

        logger.info(
            f"[HINT_GENERATION] Found {len(solutions)} accepted/modified solutions for client {client_id}"
        )

        for solution in solutions:
            prompt = (
                "The following incidents had this accepted solution. "
                "Use the AST diffs below as a guiding pattern for migration.\n\n"
                "Generate a hint for the user so that they can migrate the code.\n\n"
                "IMPORTANT: Follow this EXACT output format:\n"
                "---\n"
                "SUMMARY:\n"
                "[concise summary of necessary changes]\n\n"
                "HINT:\n"
                "[numbered steps with generic, reusable code examples]\n"
                "---\n\n"
                "Guidelines for high-quality response:\n"
                "1. Keep SUMMARY concise and focused\n"
                "2. Use numbered steps (1, 2, 3) in HINT section\n"
                "3. Provide generic before/after code examples that can be reused and mark them as examples (e.g. 'Example 1: Before: ... After: ...')\n"
                "4. Write in direct, actionable tone\n"
                "Incidents:\n"
            )

            for i, incident in enumerate(solution.incidents):
                prompt += (
                    f"Incident {i + 1}:\n"
                    f"  URI: {incident.uri}\n"
                    f"  Message: {incident.message}\n"
                    f"  Code Snippet: {incident.code_snip}\n"
                    f"  Line Number: {incident.line_number}\n"
                    f"  Variables: {incident.variables}\n"
                    f"  Violation: {incident.violation.ruleset_name} - "
                    f"  {incident.violation.violation_name}\n\n"
                )

            diff = associate_files(
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.before],
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.after],
            )

            ast_diffs: list[dict[str, Any]] = []
            for (_before_uri, _after_uri), (before_file, after_file) in diff.items():
                if before_file.content == after_file.content:
                    continue

                ast_diffs.append(
                    extract_ast_info(before_file.content, language=Language.JAVA).diff(
                        extract_ast_info(after_file.content, language=Language.JAVA)
                    )
                )

            ast_diff_str = "\n\n".join(str(a) for a in ast_diffs if a is not None)
            prompt += f"AST Diff:\n{ast_diff_str}\n\n"

            logger.debug(f"[HINT_GENERATION] Invoking LLM for solution {solution.id}")
            response = await kai_ctx.model.ainvoke(prompt)

            hint = DBHint(
                text=str(response.content),
                violations=set(
                    incident.violation
                    for incident in solution.incidents
                    if incident.violation is not None
                ),
                solutions=set([solution]),
            )
            session.add(hint)
            logger.info(
                f"[DB_STATE_CHANGE] Created hint for solution {solution.id} with {len(hint.violations)} violations"
            )

            await session.flush()

        await session.commit()
        logger.info(
            f"[HINT_GENERATION] Completed hint generation for client {client_id}"
        )


async def delete_solution(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    solution_id: int,
) -> bool:
    logger.info(
        f"[DB_STATE] Attempting to delete solution {solution_id} for client {client_id}"
    )
    async with kai_ctx.session_maker.begin() as session:
        sln = await session.get(DBSolution, solution_id)
        if sln is None:
            logger.warning(f"[DB_STATE] Solution {solution_id} not found")
            return False
        logger.info(
            f"[DB_STATE_CHANGE] Deleting solution {solution_id} with status {sln.solution_status}"
        )
        await session.delete(sln)
        await session.commit()
        logger.info(f"[DB_STATE] Solution {solution_id} deleted successfully")
    return True


@mcp.tool(name="delete_solution")
async def tool_delete_solution(
    ctx: Context,
    client_id: str,
    solution_id: int,
) -> bool:
    """
    Delete the solution with the given ID from the database.
    """
    logger.info(
        f"[REQUEST] delete_solution - client_id: {client_id}, solution_id: {solution_id}"
    )
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        result = await delete_solution(
            kai_ctx,
            client_id,
            solution_id,
        )
        logger.info(f"[RESPONSE] delete_solution - Deleted: {result}")
        return result


# TODO: Make this a resource instead of a tool. Need to figure out how to handle
# lists in a resource.


class GetBestHintResult(BaseModel):
    hint: str
    hint_id: int


async def get_best_hint(
    kai_ctx: KaiSolutionServerContext,
    ruleset_name: str,
    violation_name: str,
) -> GetBestHintResult | None:
    async with kai_ctx.session_maker.begin() as session:
        violation_name_stmt = select(DBViolation).where(
            DBViolation.ruleset_name == ruleset_name,
            DBViolation.violation_name == violation_name,
        )
        violation = (await session.execute(violation_name_stmt)).scalar_one_or_none()
        if violation is None:
            log(
                f"Violation {ruleset_name} - {violation_name} not found in the database.",
            )
            return None

        for hint in sorted(violation.hints, key=lambda h: h.created_at, reverse=True):
            if any(
                s.solution_status == SolutionStatus.ACCEPTED
                or s.solution_status == SolutionStatus.MODIFIED
                for s in hint.solutions
            ):
                return GetBestHintResult(
                    hint=hint.text or "",
                    hint_id=hint.id,
                )

    return None


@mcp.tool(name="get_best_hint")
async def tool_get_best_hint(
    ctx: Context,
    ruleset_name: str,
    violation_name: str,
) -> GetBestHintResult | None:
    """
    Get the best hint for a given ruleset and violation name.
    This function retrieves the most recent hint for the specified ruleset and
    violation name from the database. If no hint is found, it returns None.
    If a hint is found, it returns a GetBestHintResult object containing the hint text
    and the hint ID. The hint is considered the best if it has at least one solution
    with the status "accepted".
    """
    logger.info(
        f"[REQUEST] get_best_hint - ruleset: {ruleset_name}, violation: {violation_name}"
    )
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        result = await get_best_hint(
            kai_ctx,
            ruleset_name,
            violation_name,
        )
        if result:
            logger.info(f"[RESPONSE] get_best_hint - Found hint ID: {result.hint_id}")
        else:
            logger.info(f"[RESPONSE] get_best_hint - No hint found")
        return result


class SuccessRateMetric(BaseModel):
    counted_solutions: int = 0
    accepted_solutions: int = 0
    rejected_solutions: int = 0
    modified_solutions: int = 0
    pending_solutions: int = 0
    unknown_solutions: int = 0


async def get_success_rate(
    kai_ctx: KaiSolutionServerContext,
    violation_ids: list[ViolationID],
) -> list[SuccessRateMetric] | None:
    result: list[SuccessRateMetric] = []

    if len(violation_ids) == 0:
        return result

    async with kai_ctx.session_maker.begin() as session:
        violations_where = or_(  # type: ignore[arg-type]
            and_(
                DBViolation.ruleset_name == violation_id.ruleset_name,
                DBViolation.violation_name == violation_id.violation_name,
            )
            for violation_id in violation_ids
        )

        violations_stmt = select(DBViolation).where(violations_where)
        violations = (await session.execute(violations_stmt)).scalars().all()

        for violation in violations:
            metric = SuccessRateMetric()

            for incident in violation.incidents:
                if incident.solution is None:
                    continue

                # FIXME: This should be automatic, but its not
                incident.solution.update_solution_status()

                # TODO: Make this cleaner
                metric.counted_solutions += 1
                metric.accepted_solutions += int(
                    incident.solution is not None
                    and incident.solution.solution_status == SolutionStatus.ACCEPTED
                )
                metric.rejected_solutions += int(
                    incident.solution is not None
                    and incident.solution.solution_status == SolutionStatus.REJECTED
                )
                metric.modified_solutions += int(
                    incident.solution is not None
                    and incident.solution.solution_status == SolutionStatus.MODIFIED
                )
                metric.pending_solutions += int(
                    incident.solution is not None
                    and incident.solution.solution_status == SolutionStatus.PENDING
                )
                metric.unknown_solutions += int(
                    incident.solution is not None
                    and incident.solution.solution_status == SolutionStatus.UNKNOWN
                )

            result.append(metric)

    return result


# TODO: Make this a resource instead of a tool. Need to figure out how to handle
# lists in a resource.
@mcp.tool(name="get_success_rate")
async def tool_get_success_rate(
    ctx: Context,
    violation_ids: list[ViolationID],
) -> list[SuccessRateMetric] | None:
    """
    Get the success rate for a list of violations.

    This function retrieves the success rate for the given list of violations from the
    database. The success rate is calculated as the number of accepted solutions divided
    by the total number of solutions for each violation. If no violations are provided,
    an empty list is returned. If any of the violations do not exist in the database,
    they are ignored.
    """
    logger.info(
        f"[REQUEST] get_success_rate - violations: {len(violation_ids)} requested"
    )
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        result = await get_success_rate(
            kai_ctx,
            violation_ids,
        )
        if result:
            total_accepted = sum(m.accepted_solutions for m in result)
            total_counted = sum(m.counted_solutions for m in result)
            logger.info(
                f"[RESPONSE] get_success_rate - Metrics for {len(result)} violations, total accepted: {total_accepted}/{total_counted}"
            )
        return result


async def accept_file(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    solution_file: SolutionFile,
) -> None:
    logger.info(
        f"[DB_STATE] Processing accept_file for client {client_id}, file: {solution_file.uri}"
    )
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(DBSolution.client_id == client_id)
        solutions = (await session.execute(solutions_stmt)).scalars().all()
        logger.debug(
            f"[DB_STATE] Found {len(solutions)} solutions for client {client_id}"
        )

        # Files to add or remove from the solution
        files_to_update: set[tuple[DBSolution, DBFile]] = set()

        for solution in solutions:
            for file in solution.after:
                if file.uri != solution_file.uri:
                    continue

                if file.content == solution_file.content:
                    previous_status = file.status
                    file.status = SolutionStatus.ACCEPTED
                    logger.info(
                        f"[DB_STATE_CHANGE] File {file.uri} status changed: {previous_status} -> ACCEPTED"
                    )
                    continue

                files_to_update.add((solution, file))

        if len(files_to_update) != 0:
            log(
                f"Updating {len(files_to_update)} files for client {client_id} with URI {solution_file.uri}",
            )
            logger.info(
                f"[DB_STATE_CHANGE] Creating MODIFIED file for {solution_file.uri} (content changed)"
            )
            new_file = DBFile(
                client_id=client_id,
                uri=solution_file.uri,
                content=solution_file.content,
                status=SolutionStatus.MODIFIED,
                solution_before=set(),
                solution_after=set(),
            )
            session.add(new_file)
            for solution, old_file in files_to_update:
                # Remove the old file from the solution
                solution.after.remove(old_file)
                solution.after.add(new_file)

                session.add(new_file)
                session.add(solution)

        await session.flush()

        all_solutions_accepted_or_modified = True
        for solution in solutions:
            # FIXME: There is some extreme weirdness going on here. The data in the
            # database does not update when the object updates, so we have to invalidate
            # it and refresh it. Also, sometimes the solution status is not updated
            # automatically?
            session.expire(solution)
            await session.refresh(solution)
            previous_status = solution.solution_status
            solution.update_solution_status()
            session.add(solution)
            await session.flush()

            if previous_status != solution.solution_status:
                logger.info(
                    f"[DB_STATE_CHANGE] Solution {solution.id} status changed: {previous_status} -> {solution.solution_status}"
                )
            else:
                logger.debug(
                    f"[DB_STATE] Solution {solution.id} status unchanged: {solution.solution_status}"
                )

            print(
                f"Solution {solution.id} status: {solution.solution_status}",
                file=sys.stderr,
            )

            if not (
                solution.solution_status == SolutionStatus.ACCEPTED
                or solution.solution_status == SolutionStatus.MODIFIED
            ):
                all_solutions_accepted_or_modified = False
                break

        await session.commit()

    if all_solutions_accepted_or_modified:
        logger.info(
            f"[DB_STATE] All solutions for client {client_id} are ACCEPTED or MODIFIED - triggering hint generation"
        )
        asyncio.create_task(generate_hint_v3(kai_ctx, client_id))  # type: ignore[unused-awaitable, unused-ignore]
    else:
        logger.debug(
            f"[DB_STATE] Not all solutions are ACCEPTED/MODIFIED for client {client_id} - skipping hint generation"
        )


@mcp.tool(name="accept_file")
async def tool_accept_file(
    ctx: Context,
    client_id: str,
    solution_file: SolutionFile,
) -> None:
    logger.info(
        f"[REQUEST] accept_file - client_id: {client_id}, uri: {solution_file.uri}"
    )
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        result = await accept_file(
            kai_ctx,
            client_id,
            solution_file,
        )
        logger.info(f"[RESPONSE] accept_file - Completed for {solution_file.uri}")
        return result


async def reject_file(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    file_uri: str,
) -> None:
    logger.info(
        f"[DB_STATE] Processing reject_file for client {client_id}, file: {file_uri}"
    )
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(DBSolution.client_id == client_id)
        solutions = (await session.execute(solutions_stmt)).scalars().all()
        logger.debug(
            f"[DB_STATE] Found {len(solutions)} solutions for client {client_id}"
        )

        rejected_count = 0
        for solution in solutions:
            for file in solution.after:
                if file.uri != file_uri:
                    continue

                previous_status = file.status
                file.status = SolutionStatus.REJECTED
                logger.info(
                    f"[DB_STATE_CHANGE] File {file.uri} in solution {solution.id} status changed: {previous_status} -> REJECTED"
                )
                rejected_count += 1

        await session.commit()
        logger.info(
            f"[DB_STATE] Rejected {rejected_count} files with URI {file_uri} for client {client_id}"
        )


@mcp.tool(name="reject_file")
async def tool_reject_file(
    ctx: Context,
    client_id: str,
    file_uri: str,
) -> None:
    logger.info(f"[REQUEST] reject_file - client_id: {client_id}, uri: {file_uri}")
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        result = await reject_file(
            kai_ctx,
            client_id,
            file_uri,
        )
        logger.info(f"[RESPONSE] reject_file - Completed for {file_uri}")
        return result
