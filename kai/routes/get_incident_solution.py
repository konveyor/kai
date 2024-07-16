from typing import Optional

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel

from kai import llm_io_handler
from kai.kai_logging import KAI_LOG
from kai.routes.util import to_route


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
    """
    Will need to cache the incident result so that the user, when it accepts
    or rejects it knows what the heck the user is referencing

    Stateful, stores it
    """

    KAI_LOG.debug(f"post_get_incident_solution recv'd: {request}")

    params = PostGetIncidentSolutionParams.model_validate(await request.json())

    llm_output = llm_io_handler.get_incident_solution(
        request.app["incident_store"],
        request.app["model_provider"],
        request.app["solution_consumer"],
        params.application_name,
        params.ruleset_name,
        params.violation_name,
        params.incident_snip,
        params.incident_variables,
        params.file_name,
        params.file_contents,
        params.line_number,
        params.analysis_message,
        False,
    ).content

    return web.json_response(
        {
            "llm_output": llm_output,
        }
    )
