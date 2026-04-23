from fastapi import APIRouter, Depends, HTTPException, Query

from kai_mcp_solution_server.resources import KaiSolutionServerContext
from kai_mcp_solution_server.rest.dependencies import get_kai_ctx
from kai_mcp_solution_server.rest.schemas import HintSummary, PaginatedResult
from kai_mcp_solution_server.service import (
    GetBestHintResult,
    get_best_hint,
    get_hint,
    list_hints,
)

router = APIRouter(prefix="/hints", tags=["hints"])


@router.get("/", response_model=PaginatedResult[HintSummary])
async def list_hints_endpoint(
    ruleset_name: str | None = None,
    violation_name: str | None = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> PaginatedResult[HintSummary]:
    hints, total = await list_hints(
        kai_ctx,
        ruleset_name=ruleset_name,
        violation_name=violation_name,
        offset=offset,
        limit=limit,
    )
    return PaginatedResult(
        items=[HintSummary.from_db(h) for h in hints],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/best", response_model=GetBestHintResult | None)
async def get_best_hint_endpoint(
    ruleset_name: str,
    violation_name: str,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> GetBestHintResult | None:
    return await get_best_hint(kai_ctx, ruleset_name, violation_name)


@router.get("/{hint_id}", response_model=HintSummary)
async def get_hint_endpoint(
    hint_id: int,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> HintSummary:
    hint = await get_hint(kai_ctx, hint_id)
    if hint is None:
        raise HTTPException(status_code=404, detail="Hint not found")
    return HintSummary(
        id=hint.id,
        text=hint.text,
        created_at=hint.created_at,
        violation_count=len(hint.violations),
        solution_count=len(hint.solutions),
    )
