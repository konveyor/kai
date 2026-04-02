from fastapi import Request

from kai_mcp_solution_server.resources import KaiSolutionServerContext


async def get_kai_ctx(request: Request) -> KaiSolutionServerContext:
    """FastAPI dependency that retrieves the shared KaiSolutionServerContext.

    The context is stored on the app state during composite lifespan startup.
    """
    return request.app.state.kai_ctx  # type: ignore[no-any-return]
