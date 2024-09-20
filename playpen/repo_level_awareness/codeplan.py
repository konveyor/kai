#!/usr/bin/env python

from typing import Any, Generator, List, Optional, Type

from kai.service.kai_application.kai_application import UpdatedFileContent

from playpen.repo_level_awareness.api import Agent, RpcClientConfig, Task, TaskResult, ValidationStep
from playpen.repo_level_awareness.maven_validator import MavenCompileStep


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Run the CodePlan loop against a project"
    )
    parser.add_argument(
        "source_directory", help="The root directory of the project to be fixed"
    )

    args = parser.parse_args()

    config = RpcClientConfig(args.source_directory)
    codeplan(config, None)


def codeplan(
    config: RpcClientConfig,
    updated_file_content: UpdatedFileContent,
):
    whatever_agent = Agent()

    task_manager = TaskManager(
        config,
        updated_file_content,
        validators=[MavenCompileStep(config)],
        agents=[whatever_agent],
    )
    # has a list of files affected and unprocessed
    # has a list of registered validators
    # has a list of current validation errors

    for task in task_manager.get_next_task():
        task_manager.supply_result(task_manager.execute_task(task))
        # all current failing validations and all currently affected AND UNDEALT
        # WITH files

        # Can do revalidation, or use cached results or whatever


class TaskManager:
    def __init__(
        self,
        config: RpcClientConfig,
        updated_file_sssontent: UpdatedFileContent,
        validators: Optional[list[ValidationStep]] = None,
        agents: Optional[list[Agent]] = None,
    ) -> None:

        # TODO: Files maybe could become unprocessed again, but that could lead
        # to infinite looping really hard, so we're avoiding it for now. Could
        # even have like a MAX_DEPTH or something.
        self.processed_files: list[Path] = []
        self.unprocessed_files: list[Path] = []

        self.validators: list[ValidationStep] = []
        if validators is not None:
            self.validators.extend(validators)

        self.agents: list[Agent] = []
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

    def get_agent_for_task(self, task: Task) -> Agent:
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

        # Check to see if validators are stale. If so, run them
        while True:
            if self._validators_are_stale:
                validation_errors = self.run_validators()

            # pop an error of the stack of errors
            if len(validation_errors) > 0:
                err = validation_errors.pop(0)
                yield err[1]  # TODO: This is a placeholder
                continue

            # if len(self.unprocessed_files) > 0:
            #     yield Task(self.unprocessed_files.pop(0))
            #     continue

            break


if __name__ == "__main__":
    with __import__("ipdb").launch_ipdb_on_exception():
        main()
