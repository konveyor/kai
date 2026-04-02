from fastapi import APIRouter, Depends

from kai_mcp_solution_server.resources import KaiSolutionServerContext
from kai_mcp_solution_server.rest.dependencies import get_kai_ctx
from kai_mcp_solution_server.rest.schemas import (
    IngestCommitRequest,
    IngestCommitResponse,
)
from kai_mcp_solution_server.service import ingest_commit

router = APIRouter(prefix="/bulk", tags=["bulk"])


@router.post("/ingest-commit", response_model=IngestCommitResponse, status_code=201)
async def ingest_commit_endpoint(
    body: IngestCommitRequest,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> IngestCommitResponse:
    incident_ids, solution_id, collection_id = await ingest_commit(
        kai_ctx,
        client_id=body.client_id,
        incidents=body.incidents,
        before_files=body.before_files,
        after_files=body.after_files,
        reasoning=body.reasoning,
        collection_id=body.collection_id,
    )
    return IngestCommitResponse(
        incident_ids=incident_ids,
        solution_id=solution_id,
        collection_id=collection_id,
    )
