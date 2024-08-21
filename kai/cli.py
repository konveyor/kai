#!/usr/bin/python3

"""This module is intended to facilitate using Konveyor with LLMs."""

import argparse
import json
import logging
import os
import time
import traceback

from kai.constants import PATH_KAI
from kai.kai_logging import initLoggingFromConfig
from kai.kai_trace import KaiTrace
from kai.models.kai_config import KaiConfig
from kai.models.report import Report
from kai.routes.get_incident_solutions_for_file import \
    PostGetIncidentSolutionsForFileParams
from kai.service.kai_application.kai_application import KaiApplication

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Get incident solutions for a file.")

    # TODO: take multiple, maybe directories?
    parser.add_argument("path", type=str, help="The path to the file to be migrated")
    parser.add_argument(
        "-log",
        "--loglevel",
        default=os.getenv("LOG_LEVEL", "info"),
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
    parser.add_argument(
        "-d",
        "--demo-mode",
        default=(os.getenv("DEMO_MODE", "false").lower() == "true"),
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-a",
        "--application-name",
        type=str,
        default=os.path.basename(os.path.abspath(os.curdir)),
        help="The name of the application",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="./config.toml",
        help="The path to the config file",
    )
    parser.add_argument(
        "-r",
        "--report-path",
        type=str,
        help="Path to an analysis report. One of report-path or incidents are required",
    )
    parser.add_argument(
        "-i",
        "--incidents",
        type=str,
        help="JSON-formatted list of incidents. One of report-path or incidents are required",
    )
    # parser.add_argument(
    #     "--batch_mode",
    #     type=str,
    #     default=BatchMode.SINGLE_GROUP.value,
    #     help="The batch mode to use (default: SINGLE_GROUP)",
    # )
    # parser.add_argument(
    #     "--include_solved_incidents",
    #     action="store_true",
    #     help="Include solved incidents in the results",
    # )
    # parser.add_argument(
    #     "--include_llm_results",
    #     action="store_true",
    #     help="Include LLM results in the output",
    # )

    args = parser.parse_args()

    kai_application = app(args.config, args.loglevel, args.demo_mode)

    with open(args.path, "r") as f:
        file_contents = f.read()

    if args.incidents:
        incidents = json.loads(args.incidents)
    elif args.report_path:
        report = Report.load_report_from_file(args.report_path)
        impacted_files = report.get_impacted_files()
        incidents = []
        for k, v in impacted_files.items():
            if args.path.endswith(k):
                incidents = v
                break
        else:
            raise SystemExit("No incidents to fix")
            # TODO if no incidents found for file
            pass
    else:
        raise Exception("One of incidents or report-path is required")

    # TODO: figure out why these logs aren't showing
    log.info(f"Total of {len(incidents)} incidents.")

    params = PostGetIncidentSolutionsForFileParams(
        file_name=args.path,
        file_contents=file_contents,
        application_name=args.application_name,
        incidents=incidents,
        # batch_mode=BatchMode(args.batch_mode),
        # include_solved_incidents=args.include_solved_incidents,
        # include_llm_results=args.include_llm_results,
    )

    trace = KaiTrace(
        trace_enabled=kai_application.config.trace_enabled,
        log_dir=kai_application.config.log_dir,
        model_id=kai_application.model_provider.model_id,
        batch_mode=params.batch_mode,
        application_name=params.application_name,
        file_name=params.file_name,
    )

    start = time.time()
    trace.start(start)
    trace.params(params)

    try:
        result = kai_application.get_incident_solutions_for_file(
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
        log.info(
            f"END - completed in '{end-start}s:  - App: '{params.application_name}', File: '{params.file_name}' with {len(params.incidents)} incidents'"
        )

    print(result.updated_file)


def app(config_path: str, log_level: str, demo_mode: bool) -> KaiApplication:
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file not found.")

    config = KaiConfig.model_validate_filepath(os.path.join(PATH_KAI, "config.toml"))

    config.log_level = log_level
    config.demo_mode = demo_mode
    if os.getenv("TRACE") is not None:
        config.trace_enabled = os.getenv("TRACE").lower() == "true"
    if os.getenv("LOG_DIR") is not None:
        config.log_dir = os.getenv("LOG_DIR")

    initLoggingFromConfig(config)

    return KaiApplication(config)


if __name__ == "__main__":
    with __import__("ipdb").launch_ipdb_on_exception():
        main()
