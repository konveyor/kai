import time
import traceback
from enum import StrEnum
from trace import Trace
from typing import Optional

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel

from kai import llm_io_handler
from kai.kai_logging import KAI_LOG
from kai.models.analyzer_types import Incident
from kai.routes.util import to_route


class PostGetIncidentSolutionsForFileBatchMode(StrEnum):
    NONE = "none"
    SINGLE_GROUP = "single_group"
    RULESET = "ruleset"
    VIOLATION = "violation"


class PostGetIncidentSolutionsForFileParams(BaseModel):
    file_name: str
    file_contents: str
    application_name: str
    batch_mode: Optional[PostGetIncidentSolutionsForFileBatchMode] = "single_group"
    include_solved_incidents: Optional[bool] = True
    include_llm_results: Optional[bool] = False
    incidents: list[Incident]


@to_route("post", "/get_incident_solutions_for_file")
async def post_get_incident_solutions_for_file(request: Request):
    KAI_LOG.info("hello!")
    start = time.time()
    KAI_LOG.debug(f"get_incident_solutions_for_file recv'd: {request}")
    params = PostGetIncidentSolutionsForFileParams.model_validate(await request.json())

    KAI_LOG.info(
        f"START - App: '{params.application_name}', File: '{params.file_name}' with {len(params.incidents)} incidents'"
    )

    trace = Trace(
        config=request.app["config"],
        model_id=request.app["model_provider"].model_id,
        application_name=params.application_name,
        file_name=params.file_name,
        batch_mode=params.batch_mode,
    )
    trace.start(start)
    trace.params(params)

    try:
        result = await llm_io_handler.get_incident_solutions_for_file(
            trace,
            request.app["model_provider"],
            request.app["incident_store"],
            params.file_contents,
            params.file_name,
            params.application_name,
            [x.model_dump() for x in params.incidents],
            request.app["solution_consumer"],
            params.batch_mode,
            params.include_solved_incidents,
            params.include_llm_results,
            request.app["config"].demo_mode,
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

    return web.json_response(result)
