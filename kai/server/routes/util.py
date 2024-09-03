from typing import Callable

from aiohttp import web


def to_route(method: str, path: str):
    def decorator(func: Callable):
        return web.route(method, path, func)

    return decorator
