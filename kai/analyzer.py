import logging
import os
import subprocess  # trunk-ignore(bandit/B404)
import threading
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import IO, Any, Optional, cast

from opentelemetry import trace

from kai.constants import ENV, PATH_KAI
from kai.jsonrpc.core import JsonRpcServer
from kai.jsonrpc.models import JsonRpcError, JsonRpcErrorCode, JsonRpcResponse
from kai.jsonrpc.streams import BareJsonStream
from kai.logging.logging import get_logger, log

logger = get_logger(__name__)

CONST_KAI_ANALYZER_LOG_FILE = "kai-analyzer-server.log"

tracer = trace.get_tracer("analyzer_lsp")


def get_logfile_dir() -> Path:
    if not log:
        return PATH_KAI
    for h in log.handlers:
        if isinstance(h, logging.FileHandler):
            return Path(os.path.dirname(h.baseFilename))
    return PATH_KAI


def log_stderr(stderr: IO[bytes]) -> None:
    for line in iter(stderr.readline, b""):
        logger.info("analyzer_lsp rpc: " + line.decode("utf-8"))


class AnalyzerLSP:

    @tracer.start_as_current_span("initialize")
    def __init__(
        self,
        analyzer_lsp_server_binary: Path,
        repo_directory: Path,
        rules: list[Path],
        java_bundles: list[Path],
        analyzer_lsp_path: Path,
        dep_open_source_labels_path: Optional[Path],
        excluded_paths: Optional[list[Path]] = None,
        labels: Optional[str] = None,
        incident_selector: Optional[str] = None,
    ) -> None:
        self.labels = labels
        self.incident_selector = incident_selector
        """This will start an analyzer-lsp jsonrpc server"""
        # trunk-ignore-begin(bandit/B603)
        args: list[str] = [
            str(analyzer_lsp_server_binary),
            "-source-directory",
            str(repo_directory),
            "-rules",
            ",".join(map(str, rules)),
            "-lspServerPath",
            str(analyzer_lsp_path),
            "-bundles",
            ",".join(map(str, java_bundles)),
            "-log-file",
            os.path.join(get_logfile_dir(), CONST_KAI_ANALYZER_LOG_FILE),
        ]
        if dep_open_source_labels_path is not None:
            args.append("-depOpenSourceLabelsFile")
            args.append(str(dep_open_source_labels_path))
        logger.debug(f"Starting analyzer rpc server with {args}")

        try:
            self.rpc_server = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=ENV,
            )

            if self.rpc_server.poll() is not None:
                self.stop()
                raise Exception("Analyzer failed to start: process exited immediately")

            logger.debug(f"analyzer rpc server started. pid: {self.rpc_server.pid}")

            # trunk-ignore-end(bandit/B603)
            self.excluded_paths = excluded_paths

            self.stderr_logging_thread = threading.Thread(
                target=log_stderr, args=(self.rpc_server.stderr,)
            )
            self.stderr_logging_thread.start()

            self.rpc = JsonRpcServer(
                json_rpc_stream=BareJsonStream(
                    cast(BufferedReader, self.rpc_server.stdout),
                    cast(BufferedWriter, self.rpc_server.stdin),
                ),
                request_timeout=4 * 60,
                log=get_logger("kai.analyzer-rpc-client"),
            )
            self.rpc.start()
            logger.debug("analyzer rpc server started")

        except Exception as e:
            self.stop()
            raise Exception(f"Analyzer failed to start: {str(e)}") from e

    @tracer.start_as_current_span("run_analysis")
    def run_analyzer_lsp(
        self,
        label_selector: Optional[str] = None,
        included_paths: Optional[list[Path]] = None,
        incident_selector: Optional[str] = None,
        scoped_paths: Optional[list[Path]] = None,
        reset_cache: Optional[bool] = None,
    ) -> JsonRpcResponse | JsonRpcError | None:

        if label_selector is not None:
            self.labels = label_selector

        if incident_selector is not None:
            self.incident_selector = incident_selector

        request_params: dict[str, Any] = {
            "label_selector": self.labels,
            "incident_selector": self.incident_selector,
            "excluded_paths": self.excluded_paths,
        }
        if included_paths is not None:
            request_params["included_paths"] = [str(p) for p in included_paths]

        if scoped_paths is not None:
            request_params["included_paths"] = [str(p) for p in scoped_paths]

        if reset_cache:
            request_params["reset_cache"] = True

        logger.debug("Sending request to analyzer-lsp")
        logger.debug("Request params: %s", request_params)

        try:
            return self.rpc.send_request(
                "analysis_engine.Analyze",
                params=[request_params],
            )
        except Exception as e:
            logger.error(f"failed to analyze {str(e)}")
            return JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message=str(e),
            )

    def stop(self) -> None:
        logger.info("stopping analyzer")
        # This should really call the a shutdown method for the server
        # then wait for the process to be finished
        self.rpc_server.terminate()
        # self.rpc.stop()
        logger.info("ending analyzer stop")
