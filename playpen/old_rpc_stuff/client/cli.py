#!/usr/bin/env python
"""This module is intended to facilitate using Konveyor with LLMs."""

###
# Thoughts:
# This is an experiment to get a feel of what it would look like if the
# bulk of the LLM interaction moved from backend server side to in the client.
#
# The full flow is that this client may:
# - Be able to as a standalone CLI tool
# - Allow the CLI to optionally talk to Kai backend server to fetch solved
#   incident data
# - Allow the IDE to talk directly to this CLI to obtain the generated code
#   suggestion for a given file
# - Establish an agentic workflow with external integration to vet results
#   and improve quality via iterating with LLM to remediate discovered issues
# - Establish repository level planning and tracking of remediation efforts
#
#
# - Add:
# . - Allow an optional flow that can connect to Kai server to fetch solved incident info
# . - Ensure demo mode is functional
###

import argparse
import logging
import os
import pathlib
import sys
import time
import traceback
from concurrent.futures import Future, ThreadPoolExecutor, as_completed

from kai.constants import PATH_KAI
from kai.kai_logging import initLogging
from kai.kai_trace import KaiTrace
from kai.models.file_solution import parse_file_solution_content
from kai.models.kai_config import KaiConfig
from kai.models.report import Report
from kai.models.report_types import ExtendedIncident
from kai.service.kai_application.kai_application import UpdatedFileContent
from kai.service.kai_application.util import get_prompt, playback_if_demo_mode
from kai.service.llm_interfacing.model_provider import ModelProvider

log = logging.getLogger(__name__)


def get_cli_args():
    parser = argparse.ArgumentParser(description="Get incident solutions for a file.")
    parser.add_argument(
        "path", type=str, help="The path to the application to be migrated"
    )
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
        default=os.path.join(PATH_KAI, "config.toml"),
        help="The path to the config file",
    )
    parser.add_argument(
        "-r",
        "--report-path",
        type=str,
        help="Path to an analysis report.",
    )
    args = parser.parse_args()
    return args


def write_to_disk(file_path: pathlib.Path, updated_file_contents: str):
    file_path = str(file_path)  # Temporary fix for Path object

    # We expect that we are overwriting the file, so all directories should exist
    if not os.path.exists(file_path):
        log.warning(
            f"**WARNING* File {file_path} does not exist.  Proceeding, but suspect this is a new file or there is a problem with the filepath"
        )

    log.info(f"Writing updated source code to {file_path}")
    try:
        with open(file_path, "w") as f:
            f.write(updated_file_contents)
    except Exception as e:
        log.error(f"Failed to write updated_file @ {file_path} with error: {e}")
        log.error(f"Contents: {updated_file_contents}")
        sys.exit(1)


def generate_fix(
    trace,
    config,
    application_name,
    src_file_language,
    file_path,
    prompt,
    model_provider,
):
    count = 0  # later will likely add back in retry logic
    retry_attempt_count = 0
    with playback_if_demo_mode(
        config.demo_mode,
        model_provider.model_id,
        application_name,
        f'{file_path.replace("/", "-")}',
    ):
        llm_result = model_provider.llm.invoke(prompt)
        trace.llm_result(count, retry_attempt_count, llm_result)

        content = parse_file_solution_content(src_file_language, llm_result.content)

        if not content.updated_file:
            raise Exception(
                f"Error in LLM Response: The LLM did not provide an updated file for {file_path}"
            )

        result = UpdatedFileContent(
            updated_file=content.updated_file,
            total_reasoning=[content.reasoning],
            used_prompts=[prompt],
            model_id=model_provider.model_id,
            additional_information=[content.additional_info],
            llm_results=[llm_result.content],
        )

        return result


def render_prompt(
    trace,
    file_name,
    src_file_language,
    src_file_contents,
    incidents: list[ExtendedIncident],
    model_provider: ModelProvider,
) -> str:

    pb_incidents = [incident.model_dump() for incident in incidents]
    #####
    ## TODO:  Add an optional means of including solved incidents when desired
    #####
    pb_vars = {
        "src_file_name": file_name,
        "src_file_language": src_file_language,
        "src_file_contents": src_file_contents,
        "incidents": pb_incidents,
        "model_provider": model_provider,
    }
    # Render the prompt
    prompt = get_prompt(model_provider.template, pb_vars)
    trace.prompt(0, prompt, pb_vars)
    return prompt


def get_impacted_files_from_report(
    report_path: str,
) -> dict[pathlib.Path, list[ExtendedIncident]]:
    report = Report.load_report_from_file(report_path)
    return report.get_impacted_files()


def get_model_provider(config: KaiConfig) -> ModelProvider:
    model_provider = ModelProvider(config)
    return model_provider


def get_config(config_path: str) -> KaiConfig:
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file not found.")
    return KaiConfig.model_validate_filepath(config_path)


def get_trace(
    config: KaiConfig,
    model_provider: ModelProvider,
    batch_mode: str,
    application_name: str,
    file_name: str,
) -> KaiTrace:
    return KaiTrace(
        trace_enabled=config.trace_enabled,
        log_dir=config.log_dir,
        model_id=model_provider.model_id,
        batch_mode=batch_mode,
        application_name=application_name,
        file_name=file_name,
    )


def __process_file(
    config, model_provider, application_name, application_path, impacted_file, incidents
):
    print(f"Processing file: {impacted_file}")
    trace = get_trace(config, model_provider, "single", application_name, impacted_file)
    start = time.time()
    trace.start(start)
    full_path = os.path.join(application_path, impacted_file)
    with open(full_path, "r") as f:
        src_file_contents = f.read()
    prompt = render_prompt(
        trace, impacted_file, "java", src_file_contents, incidents, model_provider
    )
    try:
        result = generate_fix(
            trace,
            config,
            application_name,
            "java",
            impacted_file,
            prompt,
            model_provider,
        )
        ###
        # TODO:
        ###
        # Add a workflow to take the result and do some validation
        # Consider running TreeSitter to ensure parses OK
        # Attempt a mvn compile and grab error messages (assumes mvn was updated to compiled if quarkus)
        write_to_disk(full_path, result.updated_file)
    except Exception as e:
        trace.exception(-1, -1, e, traceback.format_exc())
        log.exception(f"Error processing file: {impacted_file}")
        # For now, continue even if we hit an exception, we will try next file
        # raise e
    finally:
        end = time.time()
        trace.end(end)
        log.info(
            f"END - completed in '{end-start}s:  - App: '{application_name}', File: '{impacted_file}' with {len(incidents)} incidents'"
        )


def process_files_parallel(
    config, model_provider, application_name, application_path, impacted_files
):
    """Parallel processing of each file in the impacted_files list"""
    num_impacted_files = len(impacted_files)
    remaining_files = num_impacted_files
    max_workers = int(os.environ.get("KAI_MAX_WORKERS", 8))
    log.info(f"Running in parallel with {max_workers} workers")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures: list[Future[str]] = []
        for _count, (file_path, incidents) in enumerate(impacted_files.items(), 1):
            future = executor.submit(
                __process_file,
                config,
                model_provider,
                application_name,
                application_path,
                file_path,
                incidents,
            )
            futures.append(future)

        for future in as_completed(futures):
            try:
                result = future.result()
                log.info(f"Result:  {result}")
            except Exception as exc:
                log.error(f"Generated an exception: {exc}")
                log.error(traceback.format_exc())
                exit(1)

            remaining_files -= 1
            log.info(
                f"{remaining_files} files remaining from total of {num_impacted_files}"
            )


def process_files_seq(
    config, model_provider, application_name, application_path, impacted_files
):
    """Sequential processing of each file in the impacted_files list"""
    subset_impacted_files = list(impacted_files.keys())[
        :2
    ]  # Limit for testing to just 2 files
    for impacted_file in subset_impacted_files:
        __process_file(
            config,
            model_provider,
            application_name,
            application_path,
            impacted_file,
            impacted_files[impacted_file],
        )


def main():
    args = get_cli_args()
    config = get_config(args.config)
    initLogging(
        config.log_level.upper(),
        config.file_log_level.upper(),
        config.log_dir,
        "kai_client.log",
    )
    model_provider = get_model_provider(config.models)
    impacted_files = get_impacted_files_from_report(args.report_path)
    print(f"Model configured: {model_provider.model_id}")
    process_files_parallel(
        config, model_provider, args.application_name, args.path, impacted_files
    )


if __name__ == "__main__":
    # with __import__("ipdb").launch_ipdb_on_exception():
    main()
