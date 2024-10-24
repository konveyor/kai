from typing import Any, Optional

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel

from kai.logging.logging import get_logger
from kai_solution_server.routes.util import to_route
from kai_solution_server.service.solution_handling.solution_types import Solution

KAI_LOG = get_logger(__name__)


class PostGetSolutionsParams(BaseModel):
    ruleset_name: str
    violation_name: str
    incident_variables: dict[str, Any]
    incident_snip: Optional[str] = None


class ResponseGetSolutions(BaseModel):
    solutions: list[Solution]


class PostSubmitAcceptedSolution(BaseModel):
    pass


@to_route("post", "/get_solutions")
async def post_get_solutions(request: Request) -> web.Response:
    KAI_LOG.debug(f"post_get_solutions recv'd: {request}")

    params = PostGetSolutionsParams.model_validate(await request.json())

    solutions: list[Solution] = request.app[
        # TODO (pgaikwad): type hint this
        "kai_incident_store"
        # web.AppKey("kai_incident_store", IncidentStore)
    ].find_solutions(**params.model_dump())

    return web.json_response(
        ResponseGetSolutions(solutions=solutions).model_dump_json()
    )


@to_route("post", "/submit_accepted_solution")
async def submit_accepted_solution(request: Request) -> web.Response:
    raise NotImplementedError("submit_accepted_solution")
