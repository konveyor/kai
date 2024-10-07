#!/usr/bin/env python

import logging
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Set

from langchain_core.language_models.chat_models import BaseChatModel

from kai.models.kai_config import KaiConfig
from kai.service.kai_application.kai_application import UpdatedFileContent
from kai.service.llm_interfacing.model_provider import ModelProvider
from playpen.repo_level_awareness.api import (
    RpcClientConfig,
    Task,
    TaskResult,
    ValidationStep,
    fuzzy_equals,
)
from playpen.repo_level_awareness.task_runner.analyzer_lsp.task_runner import (
    AnalyzerTaskRunner,
)
from playpen.repo_level_awareness.task_runner.analyzer_lsp.validator import (
    AnlayzerLSPStep,
)
from playpen.repo_level_awareness.task_runner.api import TaskRunner
from playpen.repo_level_awareness.task_runner.compiler.compiler_task_runner import (
    MavenCompilerTaskRunner,
)
from playpen.repo_level_awareness.task_runner.compiler.maven_validator import (
    MavenCompileStep,
)
from playpen.repo_level_awareness.vfs.git_vfs import RepoContextManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    import argparse

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

    args = parser.parse_args()

    config = RpcClientConfig(
        args.source_directory,
        args.analyzer_lsp_server_binary,
        args.rules_directory,
        None,
        None,
        None,
    )
    codeplan(config, None)


def codeplan(
    config: RpcClientConfig,
    updated_file_content: UpdatedFileContent,
):
    logger.info("Starting codeplan with configuration: %s", config)

    kai_config = KaiConfig.model_validate_filepath("../../kai/config.toml")
    modelProvider = ModelProvider(kai_config.models)

    # TODO: (pgaikwad) needed for reflection agent
    llm: BaseChatModel = None

    task_manager = TaskManager(
        config,
        RepoContextManager(config.repo_directory, llm=llm),
        updated_file_content,
        validators=[MavenCompileStep(config), AnlayzerLSPStep(config)],
        agents=[
            AnalyzerTaskRunner(modelProvider.llm),
            MavenCompilerTaskRunner(modelProvider.llm),
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


class TaskManager:
    def __init__(
        self,
        config: RpcClientConfig,
        rcm: RepoContextManager,
        updated_file_content: UpdatedFileContent,
        validators: Optional[list[ValidationStep]] = None,
        agents: Optional[list[TaskRunner]] = None,
    ) -> None:
        self.validators: List[ValidationStep] = []

        self.processed_files: list[Path] = []
        self.unprocessed_files: list[Path] = []

        self.processed_tasks: Set[Task] = set()
        self.task_stacks: Dict[int, List[Task]] = {}
        self.ignored_tasks: List[Task] = []

        if validators is not None:
            self.validators.extend(validators)
            logger.debug("Validators initialized: %s", self.validators)

        self.agents: list[TaskRunner] = []
        if agents is not None:
            self.agents.extend(agents)
            logger.debug("Agents initialized: %s", self.agents)

        self.config = config

        self._validators_are_stale = True

        self.rcm = rcm

        logger.info("TaskManager initialized.")

    def execute_task(self, task: Task) -> TaskResult:
        logger.info("Executing task: %s", task)
        agent = self.get_agent_for_task(task)
        logger.debug("Agent selected for task: %s", agent)
        result = agent.execute_task(self.rcm, task)
        logger.debug("Task execution result: %s", result)
        return result

    def get_agent_for_task(self, task: Task) -> TaskRunner:
        for agent in self.agents:
            if agent.can_handle_task(task):
                logger.debug("Agent %s can handle task %s", agent, task)
                return agent
        logger.error("No agent available for task: %s", task)
        raise Exception("No agent available for this task")

    def supply_result(self, result: TaskResult) -> None:
        logger.info("Supplying result: %s", result)
        for file_path in result.modified_files:
            if file_path not in self.unprocessed_files:
                self.unprocessed_files.append(file_path)
                self._validators_are_stale = True
                logger.debug("File %s marked as unprocessed.", file_path)

        if len(result.encountered_errors) > 0:
            logger.warning("Encountered errors: %s", result.encountered_errors)
            raise NotImplementedError("What should we do with errors?")

    def run_validators(self) -> list[Task]:
        logger.info("Running validators.")
        validation_tasks: List[Task] = []

        for validator in self.validators:
            logger.debug("Running validator: %s", validator)
            result = validator.run()
            logger.debug("Validator result: %s", result)
            if not result.passed:
                validation_tasks.extend(result.errors)
                logger.info("Validator %s found errors: %s", validator, result.errors)

        self._validators_are_stale = False
        logger.debug("Validators are up to date.")
        return validation_tasks

    def get_next_task(self) -> Generator[Task, Any, None]:
        prior_task = None
        self.initialize_task_stacks()
        while any(self.task_stacks.values()):
            task = self.pop_task_from_highest_priority()
            logger.debug("Popped task from stack: %s", task)
            if self.should_skip_task(task):
                logger.debug("Skipping task: %s", task)
                continue

            logger.info("Yielding task: %s", task)
            yield task
            prior_task = task
            self.handle_new_tasks_after_processing(task, prior_task)

    def initialize_task_stacks(self):
        logger.info("Initializing task stacks.")
        if self._validators_are_stale or not any(self.task_stacks.values()):
            new_tasks = self.run_validators()
            logger.debug("New tasks from validators: %s", new_tasks)
            for task in new_tasks:
                self.add_task_to_stack(task)
                logger.debug("Task %s added to stack.", task)

    def add_task_to_stack(self, task: Task):
        priority = task.priority
        if priority not in self.task_stacks:
            self.task_stacks[priority] = []
            logger.debug("Created new task stack for priority %s.", priority)
        self.task_stacks[priority].append(task)
        logger.debug("Task %s added to priority %s stack.", task, priority)

    def pop_task_from_highest_priority(self) -> Task:
        highest_priority = min(self.task_stacks.keys())
        task_stack = self.task_stacks[highest_priority]
        task = task_stack.pop()
        logger.debug("Popped task %s from priority %s stack.", task, highest_priority)
        if not task_stack:
            del self.task_stacks[highest_priority]
            logger.debug("Priority %s stack is empty and removed.", highest_priority)
        return task

    def handle_new_tasks_after_processing(
        self, task: Task, prior_task: Optional[Task] = None
    ):
        logger.info("Handling new tasks after processing task: %s", task)
        self._validators_are_stale = True
        new_tasks = self.run_validators()
        new_tasks_set = set(new_tasks)
        unprocessed_new_tasks = new_tasks_set - self.processed_tasks
        logger.debug("Unprocessed new tasks: %s", unprocessed_new_tasks)

        if unprocessed_new_tasks:
            old_tasks = list(
                filter(
                    lambda x: self.is_similar_to_prior_task(x, prior_task),
                    unprocessed_new_tasks,
                )
            )
            if len(old_tasks) == 1:
                old_task = old_tasks[0]
                unprocessed_new_tasks.remove(old_task)
                # The error may have moved slightly, we'll make sure we track the latest iteration
                # without losing any of our meta values
                old_task.priority = task.priority
                old_task.depth = task.depth
                old_task.retry_count = task.retry_count
                logger.debug("Task %s still unprocessed after execution.", task)
                self.handle_ignored_task(old_tasks[0])
            else:
                self.processed_tasks.add(task)
                logger.debug("Task %s processed successfully.", task)

            for child_task in unprocessed_new_tasks:
                child_task.parent = task
                child_task.depth = task.depth + 1
                task.children.append(child_task)
                self.add_task_to_stack(child_task)
                logger.debug("Child task %s added to stack.", child_task)
        else:
            self.processed_tasks.add(task)
            logger.debug("Task %s processed successfully.", task)

    def should_skip_task(self, task: Task) -> bool:
        skip = (
            task in self.processed_tasks
            or task in self.ignored_tasks
            and not all([self.should_skip_task(child) for child in task.children])
        )
        logger.debug("Should skip task %s: %s", task, skip)
        return skip

    def is_similar_to_prior_task(self, task: Task, prior_task: Optional[Task]) -> bool:
        if prior_task is None:
            return False
        same = prior_task == task
        logger.debug("Task %s is same to prior task %s: %s", task, prior_task, same)
        similar = fuzzy_equals(prior_task, task, offset=2)
        logger.debug(
            "Task %s is similar to prior task %s: %s", task, prior_task, similar
        )
        return same or similar

    def handle_ignored_task(self, task: Task):
        logger.info("Handling ignored task: %s", task)
        task.retry_count += 1
        if task.retry_count < task.max_retries:
            task.priority += 1
            self.add_task_to_stack(task)
            logger.debug("Retrying task %s (retry count: %s).", task, task.retry_count)
        else:
            self.ignored_tasks.append(task)
            logger.warning(
                "Task %s exceeded max retries and added to ignored tasks.", task
            )

    def stop(self):
        logger.info("Stopping TaskManager.")
        for a in self.agents:
            if hasattr(a, "stop"):
                a.stop()
                logger.debug("Stopped agent: %s", a)

        for v in self.validators:
            if hasattr(v, "stop"):
                v.stop()
                logger.debug("Stopped validator: %s", v)


if __name__ == "__main__":
    with __import__("ipdb").launch_ipdb_on_exception():
        main()
