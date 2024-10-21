from typing import Any
from aiohttp import web
from aiohttp.web_request import Request

from kai_solution_server.routes.util import to_route
from kai.logging.kai_logging import get_logger

KAI_LOG = get_logger(__name__)


@to_route("post", "/health_check")
async def post_health_check(request: Request) -> web.Response:
    KAI_LOG.debug(f"health_check recv'd: {request}")

    request_json: dict[str, Any] = await request.json()

    return web.json_response({"status": "OK!", "recv'd": request_json})
