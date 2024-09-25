#!/usr/bin/env python

from pathlib import Path
from typing import Any, Generator, Optional

from langchain_core.language_models.chat_models import BaseChatModel

from kai.models.kai_config import KaiConfig
from kai.service.kai_application.kai_application import UpdatedFileContent
from playpen.repo_level_awareness.api import (
    RpcClientConfig,
    Task,
    TaskRunner,
    TaskResult,
    ValidationStep,
    fuzzy_equals,
)
from playpen.repo_level_awareness.git_vfs import RepoContextManager
from kai.service.llm_interfacing.model_provider import ModelProvider
from playpen.repo_level_awareness.maven_validator import MavenCompileStep
from playpen.repo_level_awareness.task_runner.analyzer_lsp.validator import AnlayzerLSPStep
from playpen.repo_level_awareness.task_runner.analyzer_lsp.task_runner import AnalyzerTaskRunner


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Run the CodePlan loop against a project"
    )
    parser.add_argument(
        "source_directory", help="The root directory of the project to be fixed"
    )

    parser.add_argument(
        "rules_directory", help="The root directory of the rules to use during analysis"
    )
    
    parser.add_argument(
        "analyzer_lsp_server_binary", help="The binary for running analyzer-lsp RPC server"
    )

    args = parser.parse_args()

    config = RpcClientConfig(args.source_directory, args.analyzer_lsp_server_binary, args.rules_directory, None, None, None)
    codeplan(config, None)


def codeplan(
    config: RpcClientConfig,
    updated_file_content: UpdatedFileContent,
):
    whatever_agent = TaskRunner()

    kai_config = KaiConfig.model_validate_filepath("../../kai/config.toml")
    modelProvider = ModelProvider(kai_config.models)

    # TODO: (pgaikwad) needed for reflection agent
    llm: BaseChatModel = None

    task_manager = TaskManager(
        config,
        updated_file_content,
        validators=[MavenCompileStep(config), AnlayzerLSPStep(config)],
        agents=[whatever_agent, AnalyzerTaskRunner(modelProvider.llm)],
        rcm=RepoContextManager(config.repo_directory, llm=llm),
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

        # TODO: Files maybe could become unprocessed again, but that could lead
        # to infinite looping really hard, so we're avoiding it for now. Could
        # even have like a MAX_DEPTH or something.
        self.processed_files: list[Path] = []
        self.unprocessed_files: list[Path] = []

        self.validators: list[ValidationStep] = []
        if validators is not None:
            self.validators.extend(validators)

        self.agents: list[TaskRunner] = []
        if agents is not None:
            self.agents.extend(agents)

        self.config = config

        self._validators_are_stale = True

        # TODO: Modify the inputs to this class accordingly
        # We want all the context that went in and the result that came out too
        # updated_file_content.

        # TODO: Actually add the paths to processed and unprocessed files.

    def execute_task(self, task: Task) -> TaskResult:
        return self.get_agent_for_task(task).execute_task(task)

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

    def run_validators(self) -> list[tuple[type, Task]]:
        # NOTE: Do it this way so that in the future we could do something
        # like get all the errors in an affected file and then send THAT as
        # a task, versus locking us into, one validation error per task at a
        # time. i.e. Make it soe wae can combine validation errors into
        # single tasks. Or grabbing all errors of a type, or all errors
        # referencing a specific type.
        #
        # Basically, we're surfacing this functionality cause this whole.
        # process is going to get more complicated in the future.
        validation_errors: list[tuple[type, Task]] = []

        for validator in self.validators:
            result = validator.run()
            if not result.passed:
                validation_errors.extend((type(validator), e) for e in result.errors)

        self._validators_are_stale = False

        return validation_errors

    def get_next_task(self) -> Generator[Task, Any, None]:
        validation_errors: list[tuple[type, Task]] = []
        ignored_tasks = []

        prior_error = None
        # Check to see if validators are stale. If so, run them
        while True:
            if self._validators_are_stale:
                validation_errors = self.run_validators()

            # pop an error of the stack of errors
            if len(validation_errors) > 0:
                print(validation_errors.__len__())
                err = validation_errors.pop(0)
                if prior_error and fuzzy_equals(prior_error, err[1], offset=2):
                    ignored_tasks.append(err[1])
                    continue
                if any([fuzzy_equals(err[1], v, offset=2) for v in ignored_tasks]):
                    print(f"failed to solve error, skipping for now\n{err[1]}")
                    continue
                yield err[1]  # TODO: This is a placeholder
                prior_error = err[1]
                continue

            if len(ignored_tasks) > 0:
                # Time to give these errors another try since we've fixed everything else
                ignored_tasks = []
                continue

            # if len(self.unprocessed_files) > 0:
            #     yield Task(self.unprocessed_files.pop(0))
            #     continue

            break
    
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
