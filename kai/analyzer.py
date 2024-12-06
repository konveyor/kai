import logging
import os
import subprocess  # trunk-ignore(bandit/B404)
import threading
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import IO, Optional, cast

from kai.constants import PATH_KAI
from kai.jsonrpc.core import JsonRpcServer
from kai.jsonrpc.models import JsonRpcError, JsonRpcErrorCode, JsonRpcResponse
from kai.jsonrpc.streams import BareJsonStream
from kai.logging.logging import get_logger, log

logger = get_logger(__name__)

CONST_KAI_ANALYZER_LOG_FILE = "kai-analyzer-server.log"


def get_logfile_dir() -> str:
    if not log:
        return PATH_KAI
    for h in log.handlers:
        if isinstance(h, logging.FileHandler):
            return os.path.dirname(h.baseFilename)
    return PATH_KAI


def log_stderr(stderr: IO[bytes]) -> None:
    for line in iter(stderr.readline, b""):
        logger.info("analyzer_lsp rpc: " + line.decode("utf-8"))


class AnalyzerLSP:
    def __init__(
        self,
        analyzer_lsp_server_binary: Path,
        repo_directory: Path,
        rules_directory: Path,
        analyzer_lsp_path: Path,
        analyzer_java_bundle_path: Path,
        dep_open_source_labels_path: Optional[Path],
    ) -> None:
        """This will start and analyzer-lsp jsonrpc server"""
        # trunk-ignore-begin(bandit/B603)
        args: list[str] = [
            str(analyzer_lsp_server_binary),
            "-source-directory",
            str(repo_directory),
            "-rules-directory",
            str(rules_directory),
            "-lspServerPath",
            str(analyzer_lsp_path),
            "-bundles",
            str(analyzer_java_bundle_path),
            "-log-file",
            os.path.join(get_logfile_dir(), CONST_KAI_ANALYZER_LOG_FILE),
        ]
        if dep_open_source_labels_path is not None:
            args.append("-depOpenSourceLabelsFile")
            args.append(str(dep_open_source_labels_path))
        logger.debug(f"Starting analyzer rpc server with {args}")
        self.rpc_server = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # trunk-ignore-end(bandit/B603)

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

    def run_analyzer_lsp(
        self,
        label_selector: str,
        included_paths: list[str],
        incident_selector: str,
        scoped_paths: Optional[list[Path]] = None,
    ) -> JsonRpcResponse | JsonRpcError | None:
        request_params = {
            "label_selector": label_selector,
            "included_paths": included_paths,
            "incident_selector": incident_selector,
        }

        if scoped_paths is not None:
            request_params["included_paths"] = [str(p) for p in scoped_paths]

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
