from aiohttp.web_request import Request

from kai.routes.util import to_route


@to_route("post", "/change_model")
async def post_change_model(request: Request):
    pass
