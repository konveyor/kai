from aiohttp import web

from kai.server.routes.get_incident_solution import post_get_incident_solution
from kai.server.routes.get_incident_solutions_for_file import (
    post_get_incident_solutions_for_file,
)
from kai.server.routes.health_check import post_health_check
from kai.server.routes.load_analysis_report import post_load_analysis_report
from kai.server.routes.ws.get_incident_solution import get_ws_get_incident_solution

kai_routes: list[web.RouteDef] = [
    post_health_check,
    post_load_analysis_report,
    post_get_incident_solution,
    post_get_incident_solutions_for_file,
    get_ws_get_incident_solution,
]

__all__ = ["kai_routes"]
