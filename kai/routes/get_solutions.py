import logging
from typing import Dict, Optional

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel

from kai.routes.util import to_route

KAI_LOG = logging.getLogger(__name__)


class PostGetSolvedExamplesParams(BaseModel):
    ruleset_name: str
    violation_name: str
    incident_variables: Dict
    incident_snip: Optional[str] = None


class PostSubmitAcceptedSolution(BaseModel):
    pass


@to_route("post", "/get_solutions")
async def post_get_solutions(request: Request):
    KAI_LOG.debug(f"post_get_solutions recv'd: {request}")

    params = PostGetSolvedExamplesParams.model_validate(await request.json())

    solutions = request.app[
        # TODO (pgaikwad): type hint this
        "kai_incident_store"
        # web.AppKey("kai_incident_store", IncidentStore)
    ].find_solutions(**params.model_dump())

    return web.json_response(
        {
            "solutions": [sol.model_dump_json() for sol in solutions],
        }
    )


@to_route("post", "/submit_accepted_solution")
async def submit_accepted_solution(request: Request):
    pass
