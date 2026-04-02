from fastapi import APIRouter, Depends, HTTPException, Query

from kai_mcp_solution_server.db.python_objects import SolutionFile
from kai_mcp_solution_server.resources import KaiSolutionServerContext
from kai_mcp_solution_server.rest.dependencies import get_kai_ctx
from kai_mcp_solution_server.rest.schemas import (
    CreateIncidentRequest,
    CreateMultipleIncidentsRequest,
    IncidentDetail,
    IncidentSummary,
    PaginatedResult,
)
from kai_mcp_solution_server.service import (
    CreateIncidentResult,
    create_incident,
    get_incident,
    list_incidents,
)

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/", response_model=CreateIncidentResult, status_code=201)
async def create_incident_endpoint(
    body: CreateIncidentRequest,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> CreateIncidentResult:
    incident_id = await create_incident(kai_ctx, body.client_id, body.extended_incident)
    return CreateIncidentResult(incident_id=incident_id, solution_id=0)


@router.post("/bulk", response_model=list[CreateIncidentResult], status_code=201)
async def create_multiple_incidents_endpoint(
    body: CreateMultipleIncidentsRequest,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> list[CreateIncidentResult]:
    results: list[CreateIncidentResult] = []
    for ei in body.extended_incidents:
        incident_id = await create_incident(kai_ctx, body.client_id, ei)
        results.append(CreateIncidentResult(incident_id=incident_id, solution_id=0))
    return results


@router.get("/", response_model=PaginatedResult[IncidentSummary])
async def list_incidents_endpoint(
    client_id: str | None = None,
    ruleset_name: str | None = None,
    violation_name: str | None = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> PaginatedResult[IncidentSummary]:
    incidents, total = await list_incidents(
        kai_ctx,
        client_id=client_id,
        ruleset_name=ruleset_name,
        violation_name=violation_name,
        offset=offset,
        limit=limit,
    )
    return PaginatedResult(
        items=[IncidentSummary.from_db(i) for i in incidents],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/{incident_id}", response_model=IncidentDetail)
async def get_incident_endpoint(
    incident_id: int,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> IncidentDetail:
    incident = await get_incident(kai_ctx, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentDetail(
        id=incident.id,
        client_id=incident.client_id,
        uri=incident.uri,
        message=incident.message,
        line_number=incident.line_number,
        ruleset_name=incident.ruleset_name,
        violation_name=incident.violation_name,
        solution_id=incident.solution_id,
        code_snip=incident.code_snip,
        variables=incident.variables,
    )
