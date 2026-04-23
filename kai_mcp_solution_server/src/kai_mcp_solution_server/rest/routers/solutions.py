from fastapi import APIRouter, Depends, HTTPException, Query

from kai_mcp_solution_server.db.python_objects import SolutionFile, SolutionStatus
from kai_mcp_solution_server.resources import KaiSolutionServerContext
from kai_mcp_solution_server.rest.dependencies import get_kai_ctx
from kai_mcp_solution_server.rest.schemas import (
    AcceptFileRequest,
    CreateSolutionRequest,
    HintSummary,
    IncidentSummary,
    PaginatedResult,
    RejectFileRequest,
    SolutionDetail,
    SolutionSummary,
)
from kai_mcp_solution_server.service import (
    accept_file,
    create_solution,
    delete_solution,
    get_solution,
    list_solutions,
    reject_file,
)

router = APIRouter(prefix="/solutions", tags=["solutions"])


@router.post("/", status_code=201)
async def create_solution_endpoint(
    body: CreateSolutionRequest,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> dict[str, int]:
    solution_id = await create_solution(
        kai_ctx,
        body.client_id,
        body.incident_ids,
        body.before,
        body.after,
        body.reasoning,
        body.used_hint_ids,
    )
    return {"solution_id": solution_id}


@router.get("/", response_model=PaginatedResult[SolutionSummary])
async def list_solutions_endpoint(
    client_id: str | None = None,
    status: SolutionStatus | None = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> PaginatedResult[SolutionSummary]:
    solutions, total = await list_solutions(
        kai_ctx,
        client_id=client_id,
        status=status,
        offset=offset,
        limit=limit,
    )
    return PaginatedResult(
        items=[
            SolutionSummary(
                id=s.id,
                client_id=s.client_id,
                created_at=s.created_at,
                solution_status=s.solution_status,
                incident_count=len(s.incidents),
                reasoning=s.reasoning,
            )
            for s in solutions
        ],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/{solution_id}", response_model=SolutionDetail)
async def get_solution_endpoint(
    solution_id: int,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> SolutionDetail:
    solution = await get_solution(kai_ctx, solution_id)
    if solution is None:
        raise HTTPException(status_code=404, detail="Solution not found")
    return SolutionDetail(
        id=solution.id,
        client_id=solution.client_id,
        created_at=solution.created_at,
        solution_status=solution.solution_status,
        incident_count=len(solution.incidents),
        reasoning=solution.reasoning,
        before=[SolutionFile(uri=f.uri, content=f.content) for f in solution.before],
        after=[SolutionFile(uri=f.uri, content=f.content) for f in solution.after],
        incidents=[IncidentSummary.from_db(i) for i in solution.incidents],
        hints=[HintSummary.from_db(h) for h in solution.hints],
    )


@router.delete("/{solution_id}")
async def delete_solution_endpoint(
    solution_id: int,
    client_id: str,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> dict[str, bool]:
    result = await delete_solution(kai_ctx, client_id, solution_id)
    if not result:
        raise HTTPException(status_code=404, detail="Solution not found")
    return {"deleted": True}


@router.post("/{solution_id}/accept")
async def accept_file_endpoint(
    solution_id: int,
    body: AcceptFileRequest,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> dict[str, str]:
    await accept_file(kai_ctx, body.client_id, body.solution_file)
    return {"status": "accepted"}


@router.post("/{solution_id}/reject")
async def reject_file_endpoint(
    solution_id: int,
    body: RejectFileRequest,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> dict[str, str]:
    await reject_file(kai_ctx, body.client_id, body.file_uri)
    return {"status": "rejected"}
