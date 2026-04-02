from fastapi import APIRouter, Depends, HTTPException, Query

from kai_mcp_solution_server.resources import KaiSolutionServerContext
from kai_mcp_solution_server.rest.dependencies import get_kai_ctx
from kai_mcp_solution_server.rest.schemas import (
    AddToCollectionRequest,
    CollectionCreate,
    CollectionDetail,
    CollectionSummary,
    CollectionUpdate,
    PaginatedResult,
)
from kai_mcp_solution_server.service import (
    add_to_collection,
    create_collection,
    delete_collection,
    get_collection,
    list_collections,
    update_collection,
)

router = APIRouter(prefix="/collections", tags=["collections"])


@router.post("/", status_code=201)
async def create_collection_endpoint(
    body: CollectionCreate,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> dict[str, int]:
    collection_id = await create_collection(
        kai_ctx,
        name=body.name,
        description=body.description,
        source_repo=body.source_repo,
        migration_type=body.migration_type,
        metadata=body.metadata,
    )
    return {"collection_id": collection_id}


@router.get("/", response_model=PaginatedResult[CollectionSummary])
async def list_collections_endpoint(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> PaginatedResult[CollectionSummary]:
    collections, total = await list_collections(kai_ctx, offset=offset, limit=limit)
    return PaginatedResult(
        items=[
            CollectionSummary(
                id=c.id,
                name=c.name,
                description=c.description,
                source_repo=c.source_repo,
                migration_type=c.migration_type,
                created_at=c.created_at,
                solution_count=len(c.solutions),
                incident_count=len(c.incidents),
            )
            for c in collections
        ],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/{collection_id}", response_model=CollectionDetail)
async def get_collection_endpoint(
    collection_id: int,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> CollectionDetail:
    collection = await get_collection(kai_ctx, collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return CollectionDetail(
        id=collection.id,
        name=collection.name,
        description=collection.description,
        source_repo=collection.source_repo,
        migration_type=collection.migration_type,
        created_at=collection.created_at,
        solution_count=len(collection.solutions),
        incident_count=len(collection.incidents),
        metadata=collection.metadata_,
    )


@router.patch("/{collection_id}", response_model=CollectionDetail)
async def update_collection_endpoint(
    collection_id: int,
    body: CollectionUpdate,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> CollectionDetail:
    collection = await update_collection(
        kai_ctx,
        collection_id,
        description=body.description,
        source_repo=body.source_repo,
        migration_type=body.migration_type,
        metadata=body.metadata,
    )
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return CollectionDetail(
        id=collection.id,
        name=collection.name,
        description=collection.description,
        source_repo=collection.source_repo,
        migration_type=collection.migration_type,
        created_at=collection.created_at,
        solution_count=len(collection.solutions),
        incident_count=len(collection.incidents),
        metadata=collection.metadata_,
    )


@router.delete("/{collection_id}")
async def delete_collection_endpoint(
    collection_id: int,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> dict[str, bool]:
    result = await delete_collection(kai_ctx, collection_id)
    if not result:
        raise HTTPException(status_code=404, detail="Collection not found")
    return {"deleted": True}


@router.post("/{collection_id}/items")
async def add_to_collection_endpoint(
    collection_id: int,
    body: AddToCollectionRequest,
    kai_ctx: KaiSolutionServerContext = Depends(get_kai_ctx),
) -> dict[str, str]:
    try:
        await add_to_collection(
            kai_ctx,
            collection_id,
            solution_ids=body.solution_ids,
            incident_ids=body.incident_ids,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"status": "added"}
