#!/usr/bin/env python
import contextlib
import os
import platform
import subprocess  # trunk-ignore(bandit/B404)
import sys
import time
from io import BufferedReader, BufferedWriter
from logging import DEBUG
from pathlib import Path
from typing import Any, Generator, cast

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pydantic import BaseModel

# Ensure that we have 'kai' in our import path
sys.path.append("../../")
from kai.analyzer_types import ExtendedIncident, Report
from kai.jsonrpc.core import JsonRpcServer
from kai.jsonrpc.models import JsonRpcError, JsonRpcId, JsonRpcResponse
from kai.jsonrpc.streams import LspStyleStream
from kai.logging.logging import get_logger, init_logging_from_log_config
from kai.rpc_server.server import (
    GetCodeplanAgentSolutionParams,
    KaiRpcApplication,
    KaiRpcApplicationConfig,
)


def get_binary_path(path: str) -> Path:
    if platform.system().lower() == "windows" and ".exe" not in path.lower():
        return Path(f"{path}.exe")
    return Path(path)


SERVER_URL = "http://0.0.0.0:8080"
SAMPLE_APP_DIR = Path("coolstore")
ANALYSIS_RPC_PATH = get_binary_path("./analysis/kai-analyzer-rpc")
RPC_BINARY_PATH = get_binary_path("./analysis/kai-rpc-server")
TRACING_ENABLED = "ENABLE_TRACING"

KAI_LOG = get_logger("run_demo")

# TODOs
# 1) Add ConfigFile to tweak the server URL and rulesets/violations
# 2) Limit to specific rulesets/violations we are interested in


def pre_flight_checks() -> None:
    for path in [
        RPC_BINARY_PATH,
    ]:
        if not path.exists():
            print(
                f"Required demo component not found at path '{path}'. Make sure you have pre-requisites set up as described in https://github.com/konveyor/kai/blob/main/example/README.md"
            )
            sys.exit(1)


@contextlib.contextmanager
def initialize_rpc_server(
    config: KaiRpcApplicationConfig,
) -> Generator[JsonRpcServer, None, None]:
    # NOTE: This is a hack. Config should probably be globally accessible in
    # this script.
    global SAMPLE_APP_DIR
    SAMPLE_APP_DIR = config.root_path

    log = get_logger("client")

    rpc_subprocess = subprocess.Popen(  # trunk-ignore(bandit/B603)
        [
            RPC_BINARY_PATH,
            "--log-level",
            str(config.log_config.log_level),
            "--stderr-log-level",
            str(config.log_config.stderr_log_level),
            "--file-log-level",
            str(config.log_config.file_log_level),
            "--log-dir-path",
            config.log_config.log_dir_path,
            "--log-file-name",
            config.log_config.log_file_name,
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        env=os.environ,
    )

    log.info(rpc_subprocess.args)

    app = KaiRpcApplication()

    @app.add_notify(method="my_progress")
    def blah(
        app: KaiRpcApplication,
        server: JsonRpcServer,
        id: JsonRpcId,
        params: dict[str, Any],
    ) -> None:
        log.info(f"Received my_progress: {params}")

    rpc_server = JsonRpcServer(
        json_rpc_stream=LspStyleStream(
            cast(BufferedReader, rpc_subprocess.stdout),
            cast(BufferedWriter, rpc_subprocess.stdin),
        ),
        app=app,
        request_timeout=None,
        log=log,
    )
    rpc_server.start()

    # wait for server to start up
    time.sleep(3)

    try:
        response = rpc_server.send_request(
            method="initialize", params=config.model_dump()
        )
        if response is None:
            raise Exception("Failed to initialize RPC server, received None response")
        elif isinstance(response, JsonRpcError):
            raise Exception(
                f"Failed to initialize RPC server - {response.code} {response.message}"
            )
        elif response.error is not None:
            if isinstance(response.error, str):
                raise Exception(f"Failed to initialize RPC server - {response.error}")
            else:
                raise Exception(
                    f"Failed to initialize RPC server - {response.error.code} {response.error.message}"
                )

        yield rpc_server
    except Exception as e:
        log.error("Failed to initialize the server:", e)
    finally:
        # send shutdown
        response = rpc_server.send_request("shutdown", params={})
        log.debug(f"shutdown response -- {response}")
        log.info("Stopping RPC Server")
        rpc_subprocess.wait()
        log.info("Stopped RPC Server")
        rpc_server.stop()


class CodePlanSolutionResponse(BaseModel):
    diff: str
    modified_files: list[str]
    encountered_errors: list[str]


def apply_diff(filepath: Path, solution: CodePlanSolutionResponse) -> None:
    KAI_LOG.info(f"Writing updated source code to {filepath}")
    try:
        subprocess.run(  # trunk-ignore(bandit/B603,bandit/B607)
            ["git", "apply"],
            input=solution.diff.encode("utf-8"),
            cwd=SAMPLE_APP_DIR,
            check=True,
        )
    except Exception as e:
        KAI_LOG.error(f"Failed to write updated_file @ {filepath} with error: {e}")
        KAI_LOG.error(f"Diff: {solution.diff}")
        return


def process_file(
    server: JsonRpcServer,
    file_path: Path,
    incidents: list[ExtendedIncident],
    num_impacted_files: int,
    count: int,
) -> str:
    with trace.get_tracer("demo_tracer").start_as_current_span("process_file"):
        start = time.time()
        KAI_LOG.info(
            f"File #{count} of {num_impacted_files} - Processing {file_path} which has {len(incidents)} incidents."
        )

    params = GetCodeplanAgentSolutionParams(
        file_path=file_path,
        incidents=incidents,
        max_priority=0,
        max_depth=0,
        max_iterations=len(incidents),
        chat_token=str("123e4567-e89b-12d3-a456-426614174000"),
    )

    KAI_LOG.debug(f"Request is: {params.model_dump()}")
    response = server.send_request("getCodeplanAgentSolution", params.model_dump())
    KAI_LOG.debug(f"Response is: {response}")

    KAI_LOG.info("got response for code plan solution: %s", response)

    if isinstance(response, JsonRpcError) or response is None:
        return f"Failed to generate fix for file {params.file_path} - {response.message if response is not None else None}"
    elif isinstance(response, JsonRpcError) and response.error is not None:
        return f"Failed to generate fix for file {params.file_path} - {response.error.code} {response.error.message}"
    elif not isinstance(response, JsonRpcResponse):
        return f"Failed to generate fix for file {params.file_path} - invalid response type {type(response)}"
    try:
        solution = CodePlanSolutionResponse.model_validate(response.result)
    except Exception as e:
        return f"Failed to parse response {params.file_path} - {e}"

    apply_diff(filepath=file_path, solution=solution)

    end = time.time()
    return f"Took {end-start}s to process {file_path} with {len(incidents)} violations"


def run_demo(report: Report, server: JsonRpcServer) -> None:
    with trace.get_tracer("demo_tracer").start_as_current_span("run_demo"):
        impacted_files = report.get_impacted_files()
        sorted_file_key = list(impacted_files.keys())
        sorted_file_key.sort()
        num_impacted_files = len(impacted_files)

        total_incidents = sum(len(incidents) for incidents in impacted_files.values())
        print(
            f"{num_impacted_files} files with a total of {total_incidents} incidents."
        )

        for count, file_path in enumerate(sorted_file_key, 1):
            incidents = impacted_files[file_path]
            for incident in incidents:
                incident.uri = os.path.join(SAMPLE_APP_DIR, file_path)
                incident.uri = os.path.abspath(Path(incident.uri))

            incidents.sort()

            for incident in incidents:
                KAI_LOG.info(
                    f"incident: {incident.violation_name} --- {incident.line_number}"
                )

            process_file(
                server=server,
                incidents=incidents,
                file_path=SAMPLE_APP_DIR / file_path,
                count=count,
                num_impacted_files=num_impacted_files,
            )


def get_analysis_from_analyzer(server: JsonRpcServer) -> Report:
    params = {
        "label_selector": "(konveyor.io/target=cloud-readiness || konveyor.io/target=jakarta-ee || konveyor.io/target=jakarta-ee8 || konveyor.io/target=jakarta-ee9 || konveyor.io/target=openjdk17 || konveyor.io/target=quarkus) || (discovery)",
        "reset_cache": True,
    }
    KAI_LOG.info("setting analysis report labels: %s", params)
    response = server.send_request("analysis_engine.Analyze", params=params)
    try:
        if response is None:
            raise Exception("Analyzer LSP failed to return a result")
        elif isinstance(response, JsonRpcError):
            raise Exception(f"Analyzer output is a JsonRpcError. Error: {response}")
        elif response.result is None:
            raise Exception("Analyzer lsp's output is None")
        elif isinstance(response.result, BaseModel):
            KAI_LOG.log(DEBUG, "analyzer_output.result is a BaseModel, dumping it")
            report = response.result.model_dump()
            rulesets = report.get("Rulesets")
        else:
            KAI_LOG.log(DEBUG, "analyzer_output.result is not a BaseModel")
            KAI_LOG.log(DEBUG, response.result)
            rulesets = response.result.get("Rulesets")

        if not rulesets or not isinstance(rulesets, list):
            KAI_LOG.info("parsed zero results from validator")
            raise Exception("parsed zero results")

        report_model = Report.load_report_from_object(rulesets, "base_run")
        return report_model
    except Exception as e:
        raise Exception(f"Failed to get analysis: {e}") from e


def main() -> None:
    kai_config = KaiRpcApplicationConfig.model_validate_filepath("initialize.toml")
    init_logging_from_log_config(kai_config.log_config)
    start = time.time()

    tracer_provider: TracerProvider | None = None
    if TRACING_ENABLED in os.environ:
        resource = Resource(attributes={SERVICE_NAME: "demo"})
        tracer_provider = TracerProvider(resource=resource)
        tracer_provider.add_span_processor(
            span_processor=BatchSpanProcessor(OTLPSpanExporter())
        )
        trace.set_tracer_provider(tracer_provider=tracer_provider)

    try:
        pre_flight_checks()
        with initialize_rpc_server(kai_config) as server:
            KAI_LOG.info("starting to load report")
            report = get_analysis_from_analyzer(server)
            KAI_LOG.info("done loading report")
            run_demo(report, server)
        KAI_LOG.info(
            f"Total time to process '{SAMPLE_APP_DIR}' was {time.time()-start}s"
        )
    except Exception as e:
        KAI_LOG.error(f"Error running demo - {e}")

    if tracer_provider is not None:
        tracer_provider.force_flush()


if __name__ == "__main__":
    main()
