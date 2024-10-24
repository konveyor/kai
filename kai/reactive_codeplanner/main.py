import argparse
import logging
from pathlib import Path

from kai.kai_config import KaiConfig
from kai.reactive_codeplanner.task_manager.api import RpcClientConfig
from kai.reactive_codeplanner.task_manager.task_manager import TaskManager
from kai.reactive_codeplanner.task_runner.analyzer_lsp.task_runner import (
    AnalyzerTaskRunner,
)
from kai.reactive_codeplanner.task_runner.analyzer_lsp.validator import AnalyzerLSPStep
from kai.reactive_codeplanner.task_runner.compiler.compiler_task_runner import (
    MavenCompilerTaskRunner,
)
from kai.reactive_codeplanner.task_runner.compiler.maven_validator import (
    MavenCompileStep,
)
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager
from kai_solution_server.service.llm_interfacing.model_provider import ModelProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Run the CodePlan loop against a project"
    )
    parser.add_argument(
        "source_directory",
        help="The root directory of the project to be fixed",
        type=Path,
    )

    parser.add_argument(
        "rules_directory",
        help="The root directory of the rules to use during analysis",
        type=Path,
    )

    parser.add_argument(
        "analyzer_lsp_server_binary",
        help="The binary for running analyzer-lsp RPC server",
        type=Path,
    )

    parser.add_argument(
        "analyzer_lsp_path",
        help="The binary for analyzer-lsp",
        type=Path,
    )
    parser.add_argument(
        "analyzer_lsp_java_bundle",
        help="The path to the analyzer java bundle",
        type=Path,
    )

    parser.add_argument(
        "label_selector",
        default="",
        help="The label selector for rules",
        type=Path,
    )

    parser.add_argument(
        "incident_selector",
        default="",
        help="The incident selector for violations",
        type=Path,
    )

    args = parser.parse_args()

    config = RpcClientConfig(
        args.source_directory,
        args.analyzer_lsp_server_binary,
        args.rules_directory,
        args.analyzer_lsp_path,
        args.java_bundle_path,
        args.label_selector,
        args.incident_selector,
        None,
        # args.included_paths,
    )

    logger.info("Starting reactive codeplanner with configuration: %s", config)

    kai_config = KaiConfig.model_validate_filepath("../../kai/config.toml")
    modelProvider = ModelProvider(kai_config.models)

    task_manager = TaskManager(
        config,
        RepoContextManager(config.repo_directory),
        None,
        validators=[MavenCompileStep(config), AnalyzerLSPStep(config)],
        agents=[
            AnalyzerTaskRunner(modelProvider),
            MavenCompilerTaskRunner(modelProvider),
        ],
    )
    logger.info("TaskManager initialized with validators and agents.")

    for task in task_manager.get_next_task():
        logger.info("Received next task: %s", task)
        result = task_manager.execute_task(task)
        logger.info("Executed task: %s, Result: %s", task, result)
        task_manager.supply_result(result)
    task_manager.stop()
    logger.info("Codeplan execution completed.")


if __name__ == "__main__":
    main()
