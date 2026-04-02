from fastapi import APIRouter, Depends, HTTPException, Query

from kai_mcp_solution_server.db.python_objects import ViolationID
from kai_mcp_solution_server.resources import KaiSolutionServerContext
from kai_mcp_solution_server.rest.dependencies import get_kai_ctx
from kai_mcp_solution_server.rest.schemas import (
    HintSummary,
    IncidentSummary,
    PaginatedResult,
    ViolationDetail,
    ViolationSummary,
)
from kai_mcp_solution_server.service import (
    SuccessRateMetric,
    get_success_rate,
    get_violation,
    list_violations,
)

router = APIRouter(prefix="/violations", tags=["violations"])


@router.get("/", response_model=PaginatedResult[ViolationSummary])
async def list_violations_endpoint(
    ruleset_name: str | None = None,
    violation_name: str | None = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> PaginatedResult[ViolationSummary]:
    violations, total = await list_violations(
        kai_ctx,
        ruleset_name=ruleset_name,
        violation_name=violation_name,
        offset=offset,
        limit=limit,
    )
    return PaginatedResult(
        items=[
            ViolationSummary(
                ruleset_name=v.ruleset_name,
                violation_name=v.violation_name,
                ruleset_description=v.ruleset_description,
                violation_category=v.violation_category,
                incident_count=len(v.incidents),
                hint_count=len(v.hints),
            )
            for v in violations
        ],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/{ruleset_name}/{violation_name}", response_model=ViolationDetail)
async def get_violation_endpoint(
    ruleset_name: str,
    violation_name: str,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> ViolationDetail:
    violation = await get_violation(kai_ctx, ruleset_name, violation_name)
    if violation is None:
        raise HTTPException(status_code=404, detail="Violation not found")
    return ViolationDetail(
        ruleset_name=violation.ruleset_name,
        violation_name=violation.violation_name,
        ruleset_description=violation.ruleset_description,
        violation_category=violation.violation_category,
        incident_count=len(violation.incidents),
        hint_count=len(violation.hints),
        incidents=[IncidentSummary.from_db(i) for i in violation.incidents],
        hints=[HintSummary.from_db(h) for h in violation.hints],
    )


@router.get(
    "/{ruleset_name}/{violation_name}/success-rate",
    response_model=SuccessRateMetric | None,
)
async def get_violation_success_rate_endpoint(
    ruleset_name: str,
    violation_name: str,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> SuccessRateMetric | None:
    result = await get_success_rate(
        kai_ctx,
        [ViolationID(ruleset_name=ruleset_name, violation_name=violation_name)],
    )
    if result is None or len(result) == 0:
        return None
    return result[0]
