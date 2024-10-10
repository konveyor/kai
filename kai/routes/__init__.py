from aiohttp import web

from kai.routes.get_solutions import post_get_solutions
from kai.routes.health_check import post_health_check

kai_routes: list[web.RouteDef] = [
    post_health_check,
    post_get_solutions,
]

__all__ = ["kai_routes"]
