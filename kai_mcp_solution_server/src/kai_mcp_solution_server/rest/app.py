from fastapi import FastAPI

from kai_mcp_solution_server.rest.routers import (
    bulk,
    collections,
    health,
    hints,
    incidents,
    solutions,
    violations,
)


def create_rest_app() -> FastAPI:
    app = FastAPI(
        title="KAI Solution Server REST API",
        version="0.1.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )
    app.include_router(health.router)
    app.include_router(incidents.router)
    app.include_router(solutions.router)
    app.include_router(violations.router)
    app.include_router(hints.router)
    app.include_router(collections.router)
    app.include_router(bulk.router)
    return app
