import argparse
import time
import tomllib
from pathlib import Path
from typing import Any, Generator

import kai.logging.logging as logging
from kai.analyzer import AnalyzerLSP
from kai.llm_interfacing.model_provider import ModelProvider
from kai.reactive_codeplanner.agent.analyzer_fix.agent import AnalyzerAgent
from kai.reactive_codeplanner.agent.dependency_agent.dependency_agent import (
    MavenDependencyAgent,
)
from kai.reactive_codeplanner.agent.maven_compiler_fix.agent import MavenCompilerAgent
from kai.reactive_codeplanner.agent.reflection_agent import ReflectionAgent
from kai.reactive_codeplanner.task_manager.api import RpcClientConfig, Task
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
from kai.reactive_codeplanner.task_runner.dependency.task_runner import (
    DependencyTaskRunner,
)
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager
from kai.rpc_server.server import KaiRpcApplicationConfig

logger = logging.get_logger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the CodePlan loop against a project"
    )

    parser.add_argument(
        "--kai-config",
        "-k",
        help="The path to the kai config file",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--source-directory",
        "-s",
        help="The root directory of the project to be fixed",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--rules",
        "-r",
        help="The root directories of the rules to use during analysis",
        type=Path,
        required=True,
        nargs="+",
    )

    parser.add_argument(
        "--analyzer-lsp-server-binary",
        "-b",
        help="The binary for running analyzer-lsp RPC server",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--analyzer-lsp-path",
        "-a",
        help="The binary for analyzer-lsp",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--analyzer-lsp-java-bundles",
        "-j",
        help="The path(s) to the analyzer java bundle(s)",
        type=Path,
        required=True,
        nargs="+",
    )

    parser.add_argument(
        "--label-selector",
        "-l",
        help="The label selector for rules",
        type=str,
        default="",
    )

    parser.add_argument(
        "--incident-selector",
        "-i",
        help="The incident selector for violations",
        type=str,
        default="",
    )

    parser.add_argument(
        "--dep-open-source-labels-path",
        "-d",
        help="Path to the open source labels for dependencies file",
        type=Path,
        default=None,
    )
    args = parser.parse_args()

    config = RpcClientConfig(
        args.source_directory,
        args.analyzer_lsp_server_binary,
        args.rules,
        args.analyzer_lsp_path,
        args.analyzer_lsp_java_bundles,
        args.label_selector,
        args.incident_selector,
        None,
        # args.included_paths,
    )

    logger.info("Starting reactive codeplanner with configuration: %s", config)

    kai_config_dict = {
        **tomllib.load(open(args.kai_config, "rb")),
        "root_path": args.source_directory,
        "analyzer_lsp_lsp_path": args.analyzer_lsp_path,
        "analyzer_lsp_rules_paths": args.rules,
        "analyzer_lsp_rpc_path": args.analyzer_lsp_server_binary,
        "analyzer_lsp_java_bundle_paths": args.analyzer_lsp_java_bundles,
        "analyzer_lsp_dep_labels_path": args.dep_open_source_labels_path,
    }

    kai_config = KaiRpcApplicationConfig.model_validate(kai_config_dict)

    logging.init_logging_from_log_config(kai_config.log_config)

    model_provider = ModelProvider(kai_config.model_provider)

    analyzer = AnalyzerLSP(
        analyzer_lsp_server_binary=Path(args.analyzer_lsp_server_binary),
        repo_directory=Path(args.source_directory),
        rules=[Path(args.rules)],
        analyzer_lsp_path=Path(args.analyzer_lsp_path),
        java_bundles=[Path(args.analyzer_lsp_java_bundle)],
        dep_open_source_labels_path=(
            Path(args.dep_open_source_labels_path)
            if args.dep_open_source_labels_path
            else None
        ),
    )

    task_manager = TaskManager(
        config,
        RepoContextManager(
            config.repo_directory,
            reflection_agent=ReflectionAgent(model_provider=model_provider),
        ),
        None,
        validators=[
            MavenCompileStep(config),
            AnalyzerLSPStep(config=config, analyzer=analyzer),
        ],
        task_runners=[
            DependencyTaskRunner(
                MavenDependencyAgent(model_provider, config.repo_directory)
            ),
            AnalyzerTaskRunner(AnalyzerAgent(model_provider)),
            MavenCompilerTaskRunner(MavenCompilerAgent(model_provider=model_provider)),
        ],
    )
    logger.info("TaskManager initialized with validators and agents.")
    for task in timed_get_next_task(task_manager):
        # Measure execution time
        start_exec_time = time.time()
        result = task_manager.execute_task(task)
        exec_time = time.time() - start_exec_time
        logger.info(
            "PERFORMANCE: %.6f seconds to execute task: %s, with result: %s",
            exec_time,
            task,
            result,
        )

        # Measure result supply time
        start_supply_time = time.time()
        try:
            task_manager.supply_result(result)
        except Exception as e:
            logger.error("Failed to supply result %s: %s", result, e)

        supply_time = time.time() - start_supply_time
        logger.info("PERFORMANCE: %.6f seconds to supply result", supply_time)

        logger.info("QUEUE_STATE: START")
        try:
            queue_state = str(task_manager.priority_queue)
            for line in queue_state.splitlines():
                logger.info(f"QUEUE_STATE: {line}")
        except Exception as e:
            logger.error(f"QUEUE_STATE: {e}")
        logger.info("QUEUE_STATE: END")
        logger.info("QUEUE_STATE: SUCCESSFUL_TASKS: START")
        for task in task_manager.processed_tasks:
            logger.info(f"QUEUE_STATE: SUCCESSFUL_TASKS: {task}")
        logger.info("QUEUE_STATE: SUCCESSFUL_TASKS: END")
        logger.info("QUEUE_STATE: IGNORED_TASKS: START")
        for task in task_manager.ignored_tasks:
            logger.info(f"QUEUE_STATE: IGNORED_TASKS: {task}")
        logger.info("QUEUE_STATE: IGNORED_TASKS: END")
    task_manager.stop()
    logger.info("Codeplan execution completed.")


def timed_get_next_task(task_manager: TaskManager) -> Generator[Task, Any, None]:
    task_iter = task_manager.get_next_task()
    while True:
        start_time = time.time()
        try:
            task = next(task_iter)
            get_task_time = time.time() - start_time
            logger.info(
                "PERFORMANCE: %.6f seconds to receive next task: %s (priority=%s, depth=%s)",
                get_task_time,
                task,
                task.priority,
                task.depth,
            )
            yield task
        except StopIteration:
            break


if __name__ == "__main__":
    main()
