from aiohttp import web
from aiohttp.web_request import Request

from kai.kai_logging import KAI_LOG
from kai.routes.util import to_route


@to_route("post", "/health_check")
async def post_health_check(request: Request):
    KAI_LOG.debug(f"health_check recv'd: {request}")

    request_json: dict = await request.json()

    return web.json_response({"status": "OK!", "recv'd": request_json})
