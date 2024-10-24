#!/usr/bin/env python
import contextlib
import logging
import os
import subprocess  # trunk-ignore(bandit/B404)
import sys
import time
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import Any, Generator, cast

# Ensure that we have 'kai' in our import path
sys.path.append("../../kai")
from kai.analyzer_types import ExtendedIncident, Report
from kai.jsonrpc.core import JsonRpcServer
from kai.jsonrpc.models import JsonRpcError, JsonRpcId
from kai.jsonrpc.streams import BareJsonStream
from kai.kai_config import KaiConfig
from kai.kai_logging import formatter
from kai.rpc_server.server import (
    GetCodeplanAgentSolutionParams,
    KaiRpcApplication,
    KaiRpcApplicationConfig,
)

KAI_LOG = logging.getLogger("run_demo")

SERVER_URL = "http://0.0.0.0:8080"
APP_NAME = "coolstore"
SAMPLE_APP_DIR = Path("./coolstore")
ANALYSIS_BUNDLE_PATH = "./analysis/bundle.jar"
ANALYSIS_LSP_PATH = "./analysis/jdtls/bin/jdtls"
ANALYSIS_RPC_PATH = "./analysis/analyzer_rpc"
ANALYSIS_RULES_PATH = "./analysis/rulesets/"
ANALYSIS_DEP_LABELS_FILE = "./analysis/maven.default.index"


# TODOs
# 1) Add ConfigFile to tweak the server URL and rulesets/violations
# 2) Limit to specific rulesets/violations we are interested in


@contextlib.contextmanager
def initialize_rpc_server() -> Generator[JsonRpcServer, None, None]:
    kai_config = KaiConfig.model_validate_filepath("config.toml")

    config = KaiRpcApplicationConfig(
        process_id=None,
        demo_mode=True,
        root_path=SAMPLE_APP_DIR,
        kai_backend_url=SERVER_URL,
        log_dir_path=Path("./logs"),
        model_provider=kai_config.models,
        analyzer_lsp_java_bundle_path=Path(ANALYSIS_BUNDLE_PATH),
        analyzer_lsp_lsp_path=Path(ANALYSIS_LSP_PATH),
        analyzer_lsp_rpc_path=Path(ANALYSIS_RPC_PATH),
        analyzer_lsp_rules_path=Path(ANALYSIS_RULES_PATH),
        analyzer_dep_labels_file=Path(ANALYSIS_DEP_LABELS_FILE),
    )

    current_directory = Path(os.path.dirname(os.path.realpath(__file__)))
    rpc_binary_path = current_directory / ".." / "kai" / "rpc_server" / "main.py"
    rpc_subprocess = subprocess.Popen(  # trunk-ignore(bandit/B603,bandit/B607)
        ["python", rpc_binary_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        env=os.environ,
    )

    app = KaiRpcApplication()

    @app.add_notify(method="logMessage")
    def logMessage(
        app: KaiRpcApplication,
        server: JsonRpcServer,
        id: JsonRpcId,
        params: dict[Any, Any],
    ) -> None:
        KAI_LOG.info(str(params))
        pass

    rpc_server = JsonRpcServer(
        json_rpc_stream=BareJsonStream(
            cast(BufferedReader, rpc_subprocess.stdout),
            cast(BufferedWriter, rpc_subprocess.stdin),
        ),
        app=app,
        request_timeout=240,
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
    finally:
        rpc_subprocess.terminate()
        rpc_subprocess.wait()
        rpc_server.stop()


def process_file(
    server: JsonRpcServer,
    file_path: Path,
    incidents: list[ExtendedIncident],
    num_impacted_files: int,
    count: int,
) -> str:
    start = time.time()
    KAI_LOG.info(
        f"File #{count} of {num_impacted_files} - Processing {file_path} which has {len(incidents)} incidents."
    )

    params = GetCodeplanAgentSolutionParams(
        file_path=file_path,
        incidents=incidents,
        max_depth=1,
        max_iterations=1,
    )

    response = server.send_request("getCodeplanAgentSolution", params.model_dump())

    if isinstance(response, JsonRpcError) or response is None:
        return f"Failed to generate fix for file {params.file_path} - {response.message if response is not None else None}"
    elif isinstance(response, JsonRpcError) and response.error is not None:
        return f"Failed to generate fix for file {params.file_path} - {response.error.code} {response.error.message}"

    end = time.time()
    return f"Took {end-start}s to process {file_path} with {len(incidents)} violations"


def run_demo(report: Report, server: JsonRpcServer) -> None:
    impacted_files = report.get_impacted_files()
    num_impacted_files = len(impacted_files)

    total_incidents = sum(len(incidents) for incidents in impacted_files.values())
    print(f"{num_impacted_files} files with a total of {total_incidents} incidents.")

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
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    # logging.getLogger("jsonrpc").setLevel(logging.CRITICAL)
    KAI_LOG.addHandler(console_handler)
    KAI_LOG.setLevel(logging.DEBUG)

    start = time.time()

    coolstore_analysis_dir = "./analysis/coolstore/output.yaml"
    report = Report.load_report_from_file(coolstore_analysis_dir)
    try:
        with initialize_rpc_server() as server:
            run_demo(report, server)
        KAI_LOG.info(
            f"Total time to process '{coolstore_analysis_dir}' was {time.time()-start}s"
        )
    except Exception as e:
        KAI_LOG.error(f"Error running demo - {e}")


if __name__ == "__main__":
    main()
