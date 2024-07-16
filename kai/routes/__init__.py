from aiohttp import web

from kai.routes.change_model import post_change_model
from kai.routes.get_incident_solution import post_get_incident_solution
from kai.routes.get_incident_solutions_for_file import (
    post_get_incident_solutions_for_file,
)
from kai.routes.health_check import post_health_check
from kai.routes.load_analysis_report import post_load_analysis_report
from kai.routes.ws.get_incident_solution import get_ws_get_incident_solution

kai_routes: list[web.RouteDef] = [
    post_health_check,
    post_load_analysis_report,
    post_change_model,
    post_get_incident_solution,
    post_get_incident_solutions_for_file,
    get_ws_get_incident_solution,
]

__all__ = ["kai_routes"]
