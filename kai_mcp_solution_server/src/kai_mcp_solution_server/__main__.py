import argparse
from typing import Any

from kai_mcp_solution_server.server import mcp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the KAI MCP Solution Server",
    )
    parser.add_argument(
        "--transport", type=str, default="stdio", choices=["stdio", "streamable-http"]
    )

    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to run the server on (default: nothing)",
    )

    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Host to run the server on (default: nothing)",
    )

    parser.add_argument(
        "--mount-path",
        type=str,
        default="/",
        help="Path the MCP server is mounted behind (ie, /hub/services/kai)",
    )

    args = parser.parse_args()

    if args.transport == "stdio":
        # stdio mode: no REST API, just MCP over stdin/stdout
        mcp.run(transport="stdio")
    else:
        # HTTP mode: composite app with MCP + REST API
        import asyncio
        from collections.abc import AsyncIterator
        from contextlib import asynccontextmanager

        import uvicorn
        from starlette.applications import Starlette
        from starlette.routing import Mount

        from kai_mcp_solution_server.constants import log
        from kai_mcp_solution_server.resources import KaiSolutionServerContext
        from kai_mcp_solution_server.rest.app import create_rest_app
        from kai_mcp_solution_server.settings import SolutionServerSettings

        rest_app = create_rest_app()

        @asynccontextmanager
        async def composite_lifespan(app: Starlette) -> AsyncIterator[None]:
            log("Starting composite app lifespan")
            settings = SolutionServerSettings()
            ctx = KaiSolutionServerContext(settings)
            await ctx.create()
            # Share the context with the REST app via app.state
            rest_app.state.kai_ctx = ctx
            log("Composite app lifespan ready")
            yield
            log("Composite app lifespan shutdown")

        mcp_app = mcp.http_app(
            transport="streamable-http",
            path=args.mount_path,
        )

        composite = Starlette(
            routes=[
                Mount("/api/v1", app=rest_app),
                Mount("/", app=mcp_app),
            ],
            lifespan=composite_lifespan,
        )

        uvicorn_kwargs: dict[str, Any] = {}
        if args.host is not None:
            uvicorn_kwargs["host"] = args.host
        if args.port is not None:
            uvicorn_kwargs["port"] = args.port

        uvicorn.run(composite, **uvicorn_kwargs)
