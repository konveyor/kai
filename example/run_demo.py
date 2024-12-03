#!/usr/bin/env python
import contextlib
import os
import platform
import subprocess  # trunk-ignore(bandit/B404)
import sys
import time
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import Generator, Optional, cast

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
from kai.jsonrpc.models import JsonRpcError, JsonRpcResponse
from kai.jsonrpc.streams import BareJsonStream
from kai.kai_config import KaiConfig
from kai.logging.logging import get_logger, init_logging_from_config
from kai.rpc_server.server import (
    GetCodeplanAgentSolutionParams,
    KaiRpcApplication,
    KaiRpcApplicationConfig,
)

SERVER_URL = "http://0.0.0.0:8080"
APP_NAME = "coolstore"
SAMPLE_APP_DIR = Path("coolstore")
ANALYSIS_BUNDLE_PATH = Path(".", "analysis", "bundle.jar")
ANALYSIS_LSP_PATH = Path(".", "analysis", "jdtls", "bin", "jdtls")
ANALYSIS_RPC_PATH = Path(".", "analysis",  f"kai-analyzer-rpc{'.exe' if platform.system().lower() == 'windows' else ''}")
ANALYSIS_RULES_PATH = Path(".", "analysis", "rulesets", "default", "generated")
ANALYSIS_DEP_LABELS_FILE = Path(".", "analysis", "maven.default.index")
RPC_BINARY_PATH = Path(".", "analysis",  f"kai-rpc-server{'.exe' if platform.system().lower() == 'windows' else ''}")
TRACING_ENABLED = "ENABLE_TRACING"

KAI_LOG = get_logger("run_demo")

# TODOs
# 1) Add ConfigFile to tweak the server URL and rulesets/violations
# 2) Limit to specific rulesets/violations we are interested in


def pre_flight_checks() -> None:
    for path in [
        SAMPLE_APP_DIR,
        ANALYSIS_BUNDLE_PATH,
        ANALYSIS_LSP_PATH,
        ANALYSIS_RPC_PATH,
        ANALYSIS_DEP_LABELS_FILE,
        RPC_BINARY_PATH,
    ]:
        if not path.exists():
            print(
                f"Required demo component not found at path '{path}'. Make sure you have pre-requisites set up as described in https://github.com/konveyor/kai/blob/main/example/README.md"
            )
            sys.exit(1)


@contextlib.contextmanager
def initialize_rpc_server(
    kai_config: KaiConfig,
) -> Generator[JsonRpcServer, None, None]:

    cache_dir: Optional[Path] = None
    if kai_config.cache_dir is not None:
        cache_dir = Path(kai_config.cache_dir)

    log = get_logger("client")
    config = KaiRpcApplicationConfig(
        process_id=None,
        root_path=SAMPLE_APP_DIR,
        kai_backend_url=SERVER_URL,
        log_dir_path=Path("./logs"),
        model_provider=kai_config.models,
        demo_mode=True,
        cache_dir=cache_dir,
        analyzer_lsp_java_bundle_path=ANALYSIS_BUNDLE_PATH,
        analyzer_lsp_lsp_path=ANALYSIS_LSP_PATH,
        analyzer_lsp_rpc_path=ANALYSIS_RPC_PATH,
        analyzer_lsp_rules_path=ANALYSIS_RULES_PATH,
        analyzer_lsp_dep_labels_path=ANALYSIS_DEP_LABELS_FILE,
    )

    rpc_subprocess = subprocess.Popen(  # trunk-ignore(bandit/B603)
        [RPC_BINARY_PATH, "-c", "config.toml"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        env=os.environ,
    )

    log.info(rpc_subprocess.args)

    app = KaiRpcApplication()

    rpc_server = JsonRpcServer(
        json_rpc_stream=BareJsonStream(
            cast(BufferedReader, rpc_subprocess.stdout),
            cast(BufferedWriter, rpc_subprocess.stdin),
            log=log,
        ),
        app=app,
        # TODO(fabianvf): when bumping the iterations/depth/priority, it can increase
        # execution time significantly. We need to add some kind of keepalive signal or
        # something to prevent a low timeout from killing a properly working request.
        request_timeout=6000,
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
        yield rpc_server
    except Exception as e:
        log.error("Failed to initialize the server:", e)
    finally:
        # send shutdown
        response = rpc_server.send_request("shutdown", params={})
        log.debug(f"shutdown resposne -- {response}")
        log.info("Stopping RPC Server")
        rpc_subprocess.wait()
        log.info("Stoped RPC Server")
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
    )

    KAI_LOG.debug(f"Request is: {params.model_dump()}")
    response = server.send_request("getCodeplanAgentSolution", params.model_dump())
    KAI_LOG.debug(f"Response is: {response}")

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
        num_impacted_files = len(impacted_files)

        total_incidents = sum(len(incidents) for incidents in impacted_files.values())
        print(
            f"{num_impacted_files} files with a total of {total_incidents} incidents."
        )

        for count, (file_path, incidents) in enumerate(impacted_files.items(), 1):
            for incident in incidents:
                incident.uri = os.path.join(SAMPLE_APP_DIR, file_path)

            process_file(
                server=server,
                incidents=incidents,
                file_path=SAMPLE_APP_DIR / file_path,
                count=count,
                num_impacted_files=num_impacted_files,
            )


def main() -> None:
    kai_config = KaiConfig.model_validate_filepath("config.toml")
    init_logging_from_config(kai_config)
    start = time.time()

    tracer_provider: TracerProvider | None = None
    if TRACING_ENABLED in os.environ:
        resource = Resource(attributes={SERVICE_NAME: "demo"})
        tracer_provider = TracerProvider(resource=resource)
        tracer_provider.add_span_processor(
            span_processor=BatchSpanProcessor(OTLPSpanExporter())
        )
        trace.set_tracer_provider(tracer_provider=tracer_provider)

    coolstore_analysis_dir = "./analysis/coolstore/output.yaml"
    report = Report.load_report_from_file(coolstore_analysis_dir)
    try:
        pre_flight_checks()
        with initialize_rpc_server(kai_config=kai_config) as server:
            run_demo(report, server)
        KAI_LOG.info(
            f"Total time to process '{coolstore_analysis_dir}' was {time.time()-start}s"
        )
    except Exception as e:
        KAI_LOG.error(f"Error running demo - {e}")

    if tracer_provider is not None:
        tracer_provider.force_flush()


if __name__ == "__main__":
    main()
