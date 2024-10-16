#!/usr/bin/env python

import logging
from pathlib import Path
from typing import Any, Generator, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel, ConfigDict

from kai.models.kai_config import KaiConfig
from kai.repo_level_awareness.api import (
    RpcClientConfig,
    Task,
    TaskResult,
    ValidationStep,
    fuzzy_equals,
)
from kai.repo_level_awareness.task_runner.analyzer_lsp.task_runner import (
    AnalyzerTaskRunner,
)
from kai.repo_level_awareness.task_runner.analyzer_lsp.validator import AnalyzerLSPStep
from kai.repo_level_awareness.task_runner.api import TaskRunner
from kai.repo_level_awareness.task_runner.compiler.compiler_task_runner import (
    MavenCompilerTaskRunner,
)
from kai.repo_level_awareness.task_runner.compiler.maven_validator import (
    MavenCompileStep,
)
from kai.repo_level_awareness.vfs.git_vfs import RepoContextManager
from kai.service.llm_interfacing.model_provider import ModelProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UpdatedFileContent(BaseModel):
    updated_file: str
    total_reasoning: list[str]
    used_prompts: list[str]
    model_id: str
    additional_information: list[str]
    response_metadatas: list[dict]

    llm_results: Optional[list[str | list[str | dict]]]

    # "model_" is a Pydantic protected namespace, so we must remove it
    model_config = ConfigDict(protected_namespaces=())


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


def codeplan(config: RpcClientConfig, seed_tasks: list[Task]):
    logger.info("Starting codeplan with configuration: %s", config)

    kai_config = KaiConfig.model_validate_filepath("../../kai/config.toml")
    modelProvider = ModelProvider(kai_config.models)

    # TODO: (pgaikwad) needed for reflection agent
    llm: BaseChatModel = None

    task_manager = TaskManager(
        config,
        RepoContextManager(config.repo_directory, llm=llm),
        seed_tasks,
        validators=[MavenCompileStep(config), AnalyzerLSPStep(config)],
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
        seed_tasks: Optional[list[Task]] = None,
        validators: Optional[list[ValidationStep]] = None,
        agents: Optional[list[TaskRunner]] = None,
    ) -> None:
        self.validators: list[ValidationStep] = []

        self.processed_files: list[Path] = []
        self.unprocessed_files: list[Path] = []

        self.processed_tasks: set[Task] = set()
        self.task_stacks: dict[int, list[Task]] = {}
        self.ignored_tasks: list[Task] = []

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

        if seed_tasks:
            for task in seed_tasks:
                # Seed tasks are assumed to be of the highest priority
                task.priority = 0
                self.add_task_to_stack(task)
                logger.info("Seed task %s added to stack.", task)

        logger.info("TaskManager initialized.")

    def execute_task(self, task: Task) -> TaskResult:
        logger.info("Executing task: %s", task)
        agent = self.get_agent_for_task(task)
        logger.info("Agent selected for task: %s", agent)
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
        validation_tasks: list[Task] = []

        for validator in self.validators:
            logger.debug("Running validator: %s", validator)
            result = validator.run()
            logger.debug("Validator result: %s", result)
            if not result.passed:
                validation_tasks.extend(result.errors)
                logger.info(
                    "Found %d new tasks from validator %s",
                    len(result.errors),
                    validator,
                )
                logger.debug("Validator %s found errors: %s", validator, result.errors)

        self._validators_are_stale = False
        logger.info("Found %d new tasks from validators", len(validation_tasks))
        logger.debug("Validators are up to date.")
        return validation_tasks

    def get_next_task(
        self, max_priority: Optional[int] = None
    ) -> Generator[Task, Any, None]:
        self.initialize_task_stacks()

        while any(self.task_stacks.values()):
            task = self.pop_task_from_highest_priority()
            if max_priority is not None and task.priority > max_priority:
                # Put the task back and stop iteration
                self.add_task_to_stack(task)
                return
            logger.debug("Popped task from stack: %s", task)
            if self.should_skip_task(task):
                logger.debug("Skipping task: %s", task)
                continue

            logger.info("Yielding task: %s", task)
            yield task
            self.handle_new_tasks_after_processing(task)

    def initialize_task_stacks(self):
        logger.info("Initializing task stacks.")

        new_tasks = self.run_validators()
        for task in new_tasks:
            self.add_task_to_stack(task)

    def add_task_to_stack(self, task: Task):
        for priority_level, task_stack in self.task_stacks.items():
            if task in task_stack:
                logger.debug(
                    "Task %s already exists in priority %s stack. Existing task takes precedence.",
                    task,
                    priority_level,
                )
                # Existing task takes precedence; do not add or modify
                return

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

    def handle_new_tasks_after_processing(self, task: Task):
        logger.info("Handling new tasks after processing task: %s", task)
        self._validators_are_stale = True
        new_tasks = self.run_validators()
        new_tasks_set = set(new_tasks)
        unprocessed_new_tasks = new_tasks_set - self.processed_tasks
        logger.debug("Unprocessed new tasks: %s", unprocessed_new_tasks)

        # Identify resolved tasks to remove from stacks
        tasks_in_stacks = set().union(*self.task_stacks.values())
        resolved_tasks = tasks_in_stacks - new_tasks_set
        logger.debug("Resolved tasks to remove from stacks: %s", resolved_tasks)

        # Remove resolved tasks from the stacks and mark them as processed
        for resolved_task in resolved_tasks:
            self.remove_task_from_stacks(resolved_task)
            self.processed_tasks.add(resolved_task)
            logger.info(
                "Task %s resolved indirectly and removed from queue.", resolved_task
            )

        # Check if the current task is still unprocessed (or similar)
        similar_tasks = [
            t for t in unprocessed_new_tasks if self.is_similar_to_task(t, task)
        ]

        if similar_tasks:
            new_dupe_task = similar_tasks[0]  # Assuming only one similar task
            unprocessed_new_tasks.remove(new_dupe_task)
            logger.debug("Task %s still unprocessed after execution.", task)
            self.handle_ignored_task(task)
        else:
            self.processed_tasks.add(task)
            logger.debug("Task %s processed successfully.", task)

        new_child_tasks = unprocessed_new_tasks - tasks_in_stacks
        # We want the higher priority things at the end of the list, so when we append and pop we get the highest priority
        for child_task in sorted(
            list(new_child_tasks), key=lambda x: x.priority, reverse=True
        ):
            child_task.parent = task
            child_task.depth = task.depth + 1
            child_task.priority = task.priority
            task.children.append(child_task)
            self.add_task_to_stack(child_task)

    def remove_task_from_stacks(self, task: Task):
        for priority_level in list(self.task_stacks.keys()):
            task_stack = self.task_stacks[priority_level]
            if task in task_stack:
                task_stack.remove(task)
                logger.debug(
                    "Removed task %s from priority %s stack.", task, priority_level
                )
                if not task_stack:
                    del self.task_stacks[priority_level]
                    logger.debug(
                        "Priority %s stack is empty and removed.", priority_level
                    )
                break  # Since tasks should only be in one stack, we can break

    def should_skip_task(self, task: Task) -> bool:
        skip = (
            task in self.processed_tasks
            or task in self.ignored_tasks
            and not all([self.should_skip_task(child) for child in task.children])
        )
        logger.debug("Should skip task %s: %s", task, skip)
        return skip

    def is_similar_to_task(self, task1: Task, task2: Optional[Task]) -> bool:
        if task2 is None:
            return False
        same = task2 == task1
        logger.debug("Task %s is same to prior task %s: %s", task1, task2, same)
        # TODO(fabianvf): Give tasks the ability to provide a specific fuzzy equals function?
        similar = fuzzy_equals(task2, task1, offset=2)
        logger.debug("Task %s is similar to prior task %s: %s", task1, task2, similar)
        return same or similar

    def handle_ignored_task(self, task: Task):
        logger.info("Handling ignored task: %s", task)
        task.retry_count += 1
        if task.retry_count < task.max_retries:
            task.priority += 1
            logger.debug(
                "Task %s failed (retry count: %s), decreasing priority and attempting to add back to stack",
                task,
                task.retry_count,
            )
            self.add_task_to_stack(task)
        else:
            self.ignored_tasks.append(task)
            logger.warning(
                "Task %s exceeded max retries and added to ignored tasks.", task
            )

    def stop(self) -> None:
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
    try:
        import ipdb

        with ipdb.launch_ipdb_on_exception():
            main()

    except ImportError:
        main()
