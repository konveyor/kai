#!/usr/bin/env python

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
    # has a list of files affected and unprocessed
    # has a list of registered validators
    # has a list of current validation errors

    for task in task_manager.get_next_task():
        print(f"Next task is {type(task)}")
        task_manager.supply_result(task_manager.execute_task(task))
        # all current failing validations and all currently affected AND UNDEALT
        # WITH files

        # Can do revalidation, or use cached results or whatever
    task_manager.stop()


class TaskManager:
    def __init__(
        self,
        config: RpcClientConfig,
        rcm: RepoContextManager,
        updated_file_content: UpdatedFileContent,
        validators: Optional[list[ValidationStep]] = None,
        agents: Optional[list[TaskRunner]] = None,
    ) -> None:
        self.validators: List(ValidationStep) = []

        self.processed_files: list[Path] = []
        self.unprocessed_files: list[Path] = []

        self.processed_tasks: Set[Task] = set()
        self.task_stacks: Dict[int, List[Task]] = {}

        if validators is not None:
            self.validators.extend(validators)

        self.agents: list[TaskRunner] = []
        if agents is not None:
            self.agents.extend(agents)

        self.config = config

        self._validators_are_stale = True

        self.rcm = rcm

        # TODO: Modify the inputs to this class accordingly
        # We want all the context that went in and the result that came out too
        # updated_file_content.

        # TODO: Actually add the paths to processed and unprocessed files.

    def execute_task(self, task: Task) -> TaskResult:
        return self.get_agent_for_task(task).execute_task(self.rcm, task)

    def get_agent_for_task(self, task: Task) -> TaskRunner:
        for agent in self.agents:
            if agent.can_handle_task(task):
                return agent

        raise Exception("No agent available for this task")

    def supply_result(self, result: TaskResult) -> None:
        # One result is the filesystem changes
        # SUCCESS
        # - Did something, modified file system -> Recompute
        # - Did nothing -> Go to next task

        # another is that the agent failed
        # FAILURE
        # - Did it give us more info to feed back to the repo context
        # - It failed and gave us nothing -> >:(

        for file_path in result.modified_files:
            if file_path not in self.unprocessed_files:
                self.unprocessed_files.append(file_path)
                self._validators_are_stale = True

        if len(result.encountered_errors) > 0:
            raise NotImplementedError("What should we do with errors?")

    def run_validators(self) -> list[Task]:
        validation_tasks: List[Task] = []

        for validator in self.validators:
            result = validator.run()
            if not result.passed:
                # TODO(@fabianvf): result.errors should probably be result.tasks or something instead
                # Not all validators return errors? Maybe?
                validation_tasks.extend(
                    result.errors
                )  # Assuming result.errors are Task instances

        # TODO(@fabianvf) do we need this?
        self._validators_are_stale = False

        return validation_tasks

    def get_next_task(self) -> Generator[Task, Any, None]:
        # validation_errors: list[tuple[type, Task]] = []
        ignored_tasks = []

        prior_task = None
        self.initialize_task_stacks()
        while any(self.task_stacks.values()):
            # pop an error of the stack of errors
            task = self.pop_task_from_highest_priority()

            if task in self.processed_tasks:
                continue

            if self.has_unprocessed_children(task):
                self.handle_unprocessed_children(task)
                continue

            if fuzzy_equals(prior_task, task, offset=2):
                # TODO What to do with these now?
                ignored_tasks.append(task)

            yield task
            self.processed_tasks.add(task)
            self.handle_new_tasks_after_processing(task)
            prior_task = task
            # TODO handle clearing processed tasks at some point? THis sort of broke the ignore stuff I was doing

        self.stop()

    def initialize_task_stacks(self):
        """Initializes the task stacks by running validators and populating tasks."""
        if self._validators_are_stale or not any(self.task_stacks.values()):
            new_tasks = self.run_validators()
            for task in new_tasks:
                self.add_task_to_stack(task)

    def add_task_to_stack(self, task: Task):
        """Adds a task to its corresponding priority stack."""
        priority = task.priority
        if priority not in self.task_stacks:
            self.task_stacks[priority] = []
        self.task_stacks[priority].append(task)

    def pop_task_from_highest_priority(self) -> Task:
        """Pops a task from the highest priority stack."""
        highest_priority = min(self.task_stacks.keys())
        task_stack = self.task_stacks[highest_priority]
        task = task_stack.pop()
        if not task_stack:
            del self.task_stacks[highest_priority]
        return task

    def has_unprocessed_children(self, task: Task) -> bool:
        """Checks if the task has unprocessed child tasks."""
        return any(child not in self.processed_tasks for child in task.children)

    def handle_unprocessed_children(self, task: Task):
        """
        Handles unprocessed child tasks by re-adding the parent task to the stack
        and adding unprocessed children to their respective stacks.
        """
        self.add_task_to_stack(task)
        unprocessed_children = [
            child for child in task.children if child not in self.processed_tasks
        ]
        for child in unprocessed_children:
            self.add_task_to_stack(child)

    def handle_new_tasks_after_processing(self, task: Task):
        """
        After processing a task, reruns validators to find new tasks,
        associates them as children of the current task, and adds them to the stacks.
        """
        self._validators_are_stale = True
        new_tasks = self.run_validators()
        new_tasks_set = set(new_tasks)
        unprocessed_new_tasks = new_tasks_set - self.processed_tasks

        if unprocessed_new_tasks:
            task.children.extend(unprocessed_new_tasks)
            for child_task in unprocessed_new_tasks:
                child_task.parent = task
                child_task.depth = task.depth + 1  # Increase depth for DFS
                self.add_task_to_stack(child_task)
            # Re-add the parent task to handle its new children
            self.add_task_to_stack(task)

    def stop(self):
        """For all agents or validators, if they have a running thread stop them."""
        for a in self.agents:
            if hasattr(a, "stop"):
                a.stop()

        for v in self.validators:
            if hasattr(v, "stop"):
                v.stop()


if __name__ == "__main__":
    with __import__("ipdb").launch_ipdb_on_exception():
        main()
