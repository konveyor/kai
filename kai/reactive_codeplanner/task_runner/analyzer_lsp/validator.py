import subprocess  # trunk-ignore(bandit/B404)
import threading
from io import BufferedReader, BufferedWriter
from typing import IO, Any, cast
from urllib.parse import urlparse

from pydantic import BaseModel

from kai.analyzer_types import Report
from kai.jsonrpc.core import JsonRpcServer
from kai.jsonrpc.models import JsonRpcError, JsonRpcResponse
from kai.jsonrpc.streams import BareJsonStream
from kai.logging.logging import TRACE, get_logger
from kai.reactive_codeplanner.task_manager.api import (
    RpcClientConfig,
    ValidationError,
    ValidationException,
    ValidationResult,
    ValidationStep,
)
from kai.reactive_codeplanner.task_runner.analyzer_lsp.api import (
    AnalyzerDependencyRuleViolation,
    AnalyzerRuleViolation,
)

logger = get_logger(__name__)


def log_stderr(stderr: IO[bytes]) -> None:
    for line in iter(stderr.readline, b""):
        logger.info("analyzer_lsp rpc: " + line.decode("utf-8"))


class AnalyzerLSPStep(ValidationStep):
    def __init__(self, config: RpcClientConfig) -> None:
        """This will start and analyzer-lsp jsonrpc server"""

        # trunk-ignore-begin(bandit/B603)
        rpc_server = subprocess.Popen(
            [
                config.analyzer_lsp_server_binary,
                "-source-directory",
                config.repo_directory,
                "-rules-directory",
                config.rules_directory,
                "-lspServerPath",
                config.analyzer_lsp_path,
                "-bundles",
                config.analyzer_java_bundle_path,
                "-log-file",
                "./kai-analyzer.log",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # trunk-ignore-end(bandit/B603)

        self.stderr_logging_thread = threading.Thread(
            target=log_stderr, args=(rpc_server.stderr,)
        )
        self.stderr_logging_thread.start()

        self.rpc = JsonRpcServer(
            json_rpc_stream=BareJsonStream(
                cast(BufferedReader, rpc_server.stdout),
                cast(BufferedWriter, rpc_server.stdin),
            ),
            request_timeout=4 * 60,
        )
        self.rpc.start()

        super().__init__(config)

    def run(self) -> ValidationResult:
        logger.debug("Running analyzer-lsp")

        analyzer_output = self.__run_analyzer_lsp()

        # TODO: Possibly add messages to the results
        ValidationResult(
            passed=False,
            errors=[
                ValidationError(
                    file="", line=-1, column=-1, message="Analyzer LSP failed"
                )
            ],
        )
        if analyzer_output is None:
            raise ValidationException(message="Analyzer LSP failed to return a result")
        elif isinstance(analyzer_output, JsonRpcError):
            raise ValidationException(
                message=f"Analyzer output is a JsonRpcError. Error: {analyzer_output}"
            )
        elif analyzer_output.result is None:
            raise ValidationException(message="Analyzer lsp's output is None")
        elif isinstance(analyzer_output.result, BaseModel):
            logger.log(TRACE, "analyzer_output.result is a BaseModel, dumping it")
            logger.log(TRACE, analyzer_output.result)
            analyzer_output.result = analyzer_output.result.model_dump()
        else:
            logger.log(TRACE, "analyzer_output.result is not a BaseModel")
            logger.log(TRACE, analyzer_output.result)

        errors = self.__parse_analyzer_lsp_output(analyzer_output.result)
        return ValidationResult(
            passed=not errors, errors=cast(list[ValidationError], errors)
        )

    def __run_analyzer_lsp(self) -> JsonRpcResponse | JsonRpcError | None:
        request_params = {
            "label_selector": "konveyor.io/target=quarkus konveyor.io/target=jakarta-ee",
            "included_paths": [],
            "incident_selector": "",
        }

        if self.config.label_selector is not None:
            request_params["label_selector"] = self.config.label_selector

        if self.config.included_paths is not None:
            request_params["included_paths"] = self.config.included_paths

        if self.config.incident_selector is not None:
            request_params["incident_selector"] = self.config.incident_selector

        logger.debug("Sending request to analyzer-lsp")
        logger.debug("Request params: %s", request_params)

        return self.rpc.send_request(
            "analysis_engine.Analyze",
            params=[request_params],
        )

    def __parse_analyzer_lsp_output(
        self, analyzer_output: dict[str, Any]
    ) -> list[AnalyzerRuleViolation]:
        logger.debug("Parsing analyzer-lsp output")

        rulesets = analyzer_output.get("Rulesets")

        if not rulesets or not isinstance(rulesets, list):
            logger.info("parsed zero results from validator")
            return []

        r = Report.load_report_from_object(rulesets, "analysis_run_task_runner")

        validation_errors: list[AnalyzerRuleViolation] = []
        for _k, v in r.rulesets.items():
            for _vk, vio in v.violations.items():
                for i in vio.incidents:
                    class_to_use = AnalyzerRuleViolation
                    if "pom.xml" in i.uri:
                        class_to_use = AnalyzerDependencyRuleViolation
                    validation_errors.append(
                        class_to_use(
                            file=urlparse(i.uri).path,
                            line=i.line_number,
                            column=-1,
                            message=i.message,
                            incident=i,
                            violation=vio,
                            ruleset=v,
                        )
                    )

        return validation_errors

    def stop(self) -> None:
        self.stderr_logging_thread.join()
        self.rpc.stop()
