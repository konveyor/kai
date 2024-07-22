import logging
import time
import traceback
from unittest.mock import MagicMock

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel

from kai.models.report_types import ExtendedIncident
from kai.routes.util import to_route
from kai.service.kai_application.kai_application import UpdatedFileContent
from kai.service.kai_application.util import BatchMode

KAI_LOG = logging.getLogger(__name__)

Trace = MagicMock()  # FIXME: Re-implement tracing


class PostGetIncidentSolutionsForFileParams(BaseModel):
    file_name: str
    file_contents: str
    application_name: str
    incidents: list[ExtendedIncident]

    batch_mode: BatchMode = "single_group"
    include_solved_incidents: bool = True
    include_llm_results: bool = False


@to_route("post", "/get_incident_solutions_for_file")
async def post_get_incident_solutions_for_file(request: Request):
    start = time.time()
    KAI_LOG.debug(f"get_incident_solutions_for_file recv'd: {request}")
    params = PostGetIncidentSolutionsForFileParams.model_validate(await request.json())

    KAI_LOG.info(
        f"START - App: '{params.application_name}', File: '{params.file_name}' with {len(params.incidents)} incidents'"
    )

    trace = Trace(
        # config=request.app["config"],
        # model_id=request.app["model_provider"].model_id,
        application_name=params.application_name,
        file_name=params.file_name,
        batch_mode=params.batch_mode,
    )
    trace.start(start)
    trace.params(params)

    try:
        result: UpdatedFileContent = request.app[
            "kai_application"
        ].get_incident_solutions_for_file(
            file_name=params.file_name,
            file_contents=params.file_contents,
            application_name=params.application_name,
            incidents=params.incidents,
            batch_mode=params.batch_mode,
            include_solved_incidents=params.include_solved_incidents,
            include_llm_results=params.include_llm_results,
        )
    except Exception as e:
        trace.exception(-1, -1, e, traceback.format_exc())
        raise e
    finally:
        end = time.time()
        trace.end(end)
        KAI_LOG.info(
            f"END - completed in '{end-start}s:  - App: '{params.application_name}', File: '{params.file_name}' with {len(params.incidents)} incidents'"
        )

    return web.json_response(result.model_dump_json())
