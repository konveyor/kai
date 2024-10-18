from typing import Callable

from aiohttp import web
from aiohttp.web_routedef import RouteDef, _HandlerType


def to_route(method: str, path: str) -> Callable[[_HandlerType], RouteDef]:
    def decorator(func: _HandlerType) -> RouteDef:
        return web.route(method, path, func)

    return decorator
