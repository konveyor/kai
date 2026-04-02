from fastapi import APIRouter, Depends
from sqlalchemy import text

from kai_mcp_solution_server.resources import KaiSolutionServerContext
from kai_mcp_solution_server.rest.dependencies import get_kai_ctx

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> dict[str, str]:
    if kai_ctx.session_maker is None:
        return {"status": "not ready"}
    try:
        async with kai_ctx.session_maker.begin() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}
