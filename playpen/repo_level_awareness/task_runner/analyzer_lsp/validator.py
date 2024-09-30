import subprocess  # trunk-ignore(bandit/B404)
from typing import Dict, List
from urllib.parse import urlparse

from kai.models.report import Report
from playpen.client import anlalyzer_rpc as analyzer_rpc
from playpen.repo_level_awareness.api import (
    RpcClientConfig,
    ValidationResult,
    ValidationStep,
)
from playpen.repo_level_awareness.task_runner.analyzer_lsp.api import (
    AnalyzerRuleViolation,
)


class AnlayzerLSPStep(ValidationStep):

    rpc: analyzer_rpc.AnalyzerRpcServer

    def __init__(self, RpcClientConfig: RpcClientConfig) -> None:
        """This will start and analyzer-lsp jsonrpc server"""

        # trunk-ignore-begin(bandit/B603)
        rpc_server = subprocess.Popen(
            [
                RpcClientConfig.analyzer_lsp_server_binary,
                "-source-directory",
                RpcClientConfig.repo_directory,
                "-rules-directory",
                RpcClientConfig.rules_directory,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        # trunk-ignore-end(bandit/B603)

        self.rpc = analyzer_rpc.AnalyzerRpcServer(
            json_rpc_endpoint=analyzer_rpc.AnlayzerRPCEndpoint(
                rpc_server.stdin, rpc_server.stdout
            ),
            timeout=60,
        )
        self.rpc.start()

        super().__init__(RpcClientConfig)

    def run(self) -> ValidationResult:
        analyzer_output = self.__run_analyzer_lsp()
        print(type(analyzer_output))
        errors = self.__parse_analyzer_lsp_output(analyzer_output)
        return ValidationResult(passed=not errors, errors=errors)

    def __run_analyzer_lsp(self) -> List[AnalyzerRuleViolation]:

        request_params = {
            "label_selector": "konveyor.io/target=quarkus",
            "included_paths": [],
            "incident_selector": "",
        }
        if self.config.label_selector is not None:
            request_params.LabelSelector = self.config.label_selector

        if self.config.included_paths is not None:
            request_params.IncludedPaths = self.config.included_paths

        if self.config.incident_selector is not None:
            request_params.IncidentSelector = self.config.incident_selector

        return self.rpc.call_method(
            "analysis_engine.Analyze",
            kwargs=request_params,
        )

    def __parse_analyzer_lsp_output(
        self, analyzer_output: Dict[str, any]
    ) -> List[AnalyzerRuleViolation]:
        rulesets = analyzer_output.get("Rulesets")

        if not rulesets or not isinstance(rulesets, list):
            print(f"here rulesets: {rulesets}")
            return []

        r = Report.load_report_from_object(rulesets, "analysis_run_task_runner")

        validation_errors: List[AnalyzerRuleViolation] = []
        for k, v in r.rulesets.items():
            print(f"ruleset: {k}")

            for vk, vio in v.violations.items():
                print(f"violation {vk} -- {vio.incidents.__len__()}")
                for i in vio.incidents:
                    validation_errors.append(
                        AnalyzerRuleViolation(
                            file=urlparse(i.uri).path,
                            line=i.line_number,
                            column=None,
                            message=i.message,
                            incident=i,
                            violation=vio,
                            ruleset=v,
                        )
                    )

        return validation_errors

    def stop(self):
        self.rpc.stop()
