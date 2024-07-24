import logging
import time
import traceback

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel

from kai.kai_trace import KaiTrace
from kai.models.report_types import ExtendedIncident
from kai.routes.util import to_route
from kai.service.kai_application.kai_application import (
    KaiApplication,
    UpdatedFileContent,
)
from kai.service.kai_application.util import BatchMode

KAI_LOG = logging.getLogger(__name__)


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

    kai_application: KaiApplication = request.app["kai_application"]

    trace = KaiTrace(
        trace_enabled=kai_application.config.trace_enabled,
        log_dir=kai_application.config.log_dir,
        model_id=kai_application.model_provider.model_id,
        batch_mode=params.batch_mode,
        application_name=params.application_name,
        file_name=params.file_name,
    )

    trace.start(start)
    trace.params(params)

    try:
        result: UpdatedFileContent = kai_application.get_incident_solutions_for_file(
            file_name=params.file_name,
            file_contents=params.file_contents,
            application_name=params.application_name,
            incidents=params.incidents,
            batch_mode=params.batch_mode,
            include_solved_incidents=params.include_solved_incidents,
            include_llm_results=params.include_llm_results,
            trace=trace,
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
