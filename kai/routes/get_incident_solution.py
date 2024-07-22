import logging
from typing import Optional

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel

from kai.routes.util import to_route
from kai.service.kai_application.kai_application import KaiApplication

KAI_LOG = logging.getLogger(__name__)


class PostGetIncidentSolutionParams(BaseModel):
    application_name: str
    ruleset_name: str
    violation_name: str
    incident_snip: Optional[str] = ""
    incident_variables: dict
    file_name: str
    file_contents: str
    line_number: int  # 0-indexed
    analysis_message: Optional[str] = ""


@to_route("post", "/get_incident_solution")
async def post_get_incident_solution(request: Request):
    KAI_LOG.debug(f"post_get_incident_solution recv'd: {request}")

    params = PostGetIncidentSolutionParams.model_validate(await request.json())

    llm_output = (
        request.app[web.AppKey("kai_application", KaiApplication)]
        .get_incident_solution(
            stream=False,
            **params.model_dump(),
        )
        .content
    )

    return web.json_response(
        {
            "llm_output": llm_output,
        }
    )
