#!/usr/bin/python3

"""This module is intended to facilitate using Konveyor with LLMs."""

import argparse
import datetime
import json
import os
import pprint
import time
import traceback
from enum import Enum
from trace import Trace
from typing import Optional

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel

from kai import llm_io_handler
from kai.constants import PATH_KAI
from kai.kai_logging import KAI_LOG
from kai.model_provider import ModelProvider
from kai.models.analyzer_types import Incident
from kai.models.kai_config import KaiConfig
from kai.report import Report
from kai.service.incident_store.incident_store import Application, IncidentStore

# TODO: Make openapi spec for everything

# TODO: Repo lives both on client and on server. Determine either A) Best way to
# rectify differences or B) Only have the code on one and pass stuff between
# each other
# - can be solved by getting last common commits and then applying a git diff in
#   the same manner as `git stash apply`


routes = web.RouteTableDef()

JSONSCHEMA_DIR = os.path.join(
    os.path.dirname(__file__),
    "data/jsonschema/",
)


@routes.post("/health_check")
async def post_dummy_json_request(request: Request):
    KAI_LOG.debug(f"health_check recv'd: {request}")

    request_json: dict = await request.json()

    return web.json_response({"status": "OK!", "recv'd": request_json})


# NOTE(@JonahSussman): This class can be removed if the other Application Class
# inherits from BaseModel.
class PostLoadAnalysisReportApplication(BaseModel):
    application_name: str
    repo_uri_origin: str
    repo_uri_local: str
    current_branch: str
    current_commit: str
    generated_at: datetime.datetime


class PostLoadAnalysisReportParams(BaseModel):
    path_to_report: str
    application: PostLoadAnalysisReportApplication


@routes.post("/load_analysis_report")
async def post_load_analysis_report(request: Request):
    params = PostLoadAnalysisReportParams.model_validate(await request.json())

    application = Application(**params.application.model_dump())
    report = Report.load_report_from_file(params.path_to_report)

    count = request.app["incident_store"].load_report(application, report)

    return web.json_response(
        {
            "number_new_incidents": count[0],
            "number_unsolved_incidents": count[1],
            "number_solved_incidents": count[2],
        }
    )


@routes.post("/change_model")
async def post_change_model(request: Request):
    pass


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


@routes.post("/get_incident_solution")
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


# TODO(@JonahSussman): Figure out proper pydantic model validation for this
# function
@routes.get("/ws/get_incident_solution")
async def ws_get_incident_solution(request: Request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    msg = await ws.receive()

    if msg.type == web.WSMsgType.TEXT:
        try:
            request_json = json.loads(msg.data)

            chunks = llm_io_handler.get_incident_solution(
                request.app["incident_store"],
                request.app["model_provider"],
                application_name=request_json["application_name"],
                ruleset_name=request_json["ruleset_name"],
                violation_name=request_json["violation_name"],
                incident_snip=request_json.get("incident_snip", ""),
                incident_vars=request_json["incident_variables"],
                file_name=request_json["file_name"],
                file_contents=request_json["file_contents"],
                line_number=request_json["line_number"],
                analysis_message=request_json.get("analysis_message", ""),
                stream=True,
            )

            for chunk in chunks:
                await ws.send_str(
                    json.dumps(
                        {
                            "content": chunk.content,
                        }
                    )
                )

        except json.JSONDecodeError:
            await ws.send_str(json.dumps({"error": "Received non-json data"}))

    elif msg.type == web.WSMsgType.ERROR:
        await ws.send_str(
            json.dumps({"error": f"Websocket closed with exception {ws.exception()}"})
        )
    else:
        await ws.send_str(json.dumps({"error": "Unsupported message type"}))

    await ws.close()

    return ws


class PostGetIncidentSolutionsForFileBatchMode(str, Enum):
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


@routes.post("/get_incident_solutions_for_file")
async def get_incident_solutions_for_file(request: Request):
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


def app():
    webapp = web.Application()

    config: KaiConfig
    if os.path.exists(os.path.join(PATH_KAI, "config.toml")):
        config = KaiConfig.model_validate_filepath(
            os.path.join(PATH_KAI, "config.toml")
        )
    # NOTE(@JonahSussman): For the future in case we switch to supporting yaml
    # configs.

    # elif os.path.exists(os.path.join(PATH_KAI_ROOT, "config.yaml")):
    #     config = KaiConfig.model_validate_filepath(
    #         os.path.join(PATH_KAI_ROOT, "config.yaml"))
    else:
        raise FileNotFoundError("Config file not found.")

    if os.getenv("LOGLEVEL") is not None:
        config.log_level = os.getenv("LOGLEVEL").upper()
    if os.getenv("DEMO_MODE") is not None:
        config.demo_mode = os.getenv("DEMO_MODE").lower() == "true"
    if os.getenv("TRACE") is not None:
        config.trace_enabled = os.getenv("TRACE").lower() == "true"

    print(f"Config loaded: {pprint.pformat(config)}")

    config: KaiConfig
    webapp["config"] = config

    KAI_LOG.setLevel(config.log_level.upper())
    print(
        f"Logging for KAI has been initialized and the level set to {config.log_level.upper()}"
    )

    KAI_LOG.info(
        f"Tracing of actions is {'enabled' if config.trace_enabled else 'disabled'}"
    )

    if config.demo_mode:
        KAI_LOG.info("DEMO_MODE is enabled. LLM responses will be cached")

    webapp["model_provider"] = ModelProvider(config.models)
    KAI_LOG.info(f"Selected provider: {config.models.provider}")
    KAI_LOG.info(f"Selected model: {webapp['model_provider'].model_id}")

    webapp["incident_store"] = IncidentStore.from_config(
        config.incident_store, webapp["model_provider"]
    )
    KAI_LOG.info(f"Selected incident store: {config.incident_store.provider}")

    webapp.add_routes(routes)

    return webapp


def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "-log",
        "--loglevel",
        default=os.getenv("KAI_LOG_LEVEL", "info"),
        choices=["debug", "info", "warning", "error", "critical"],
        help="""Provide logging level.
Options:
- debug: Detailed information, typically of interest only when diagnosing problems.
- info: Confirmation that things are working as expected.
- warning: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
- error: Due to a more serious problem, the software has not been able to perform some function.
- critical: A serious error, indicating that the program itself may be unable to continue running.
Example: --loglevel debug (default: warning)""",
    )

    arg_parser.add_argument(
        "-demo",
        "--demo_mode",
        default=(os.getenv("DEMO_MODE").lower() == "true"),
        action=argparse.BooleanOptionalAction,
    )

    args, _ = arg_parser.parse_known_args()

    os.environ["LOGLEVEL"] = str(args.loglevel)
    os.environ["DEMO_MODE"] = str(args.demo_mode).lower()

    web.run_app(app())


if __name__ == "__main__":
    main()
