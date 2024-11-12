#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Generator, Optional

import kai.logging.logging as logging
from kai.reactive_codeplanner.task_manager.api import (
    RpcClientConfig,
    Task,
    TaskResult,
    ValidationResult,
    ValidationStep,
)
from kai.reactive_codeplanner.task_manager.priority_queue import PriorityTaskQueue
from kai.reactive_codeplanner.task_runner.api import TaskRunner
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager

logger = logging.get_logger(__name__)


class TaskManager:
    def __init__(
        self,
        config: RpcClientConfig,
        rcm: RepoContextManager,
        seed_tasks: Optional[list[Task]] = None,
        validators: Optional[list[ValidationStep]] = None,
        task_runners: Optional[list[TaskRunner]] = None,
    ) -> None:
        self.validators: list[ValidationStep] = []

        self.processed_files: list[Path] = []
        self.unprocessed_files: list[Path] = []

        self.processed_tasks: set[Task] = set()
        self.ignored_tasks: list[Task] = []
        self.priority_queue: PriorityTaskQueue = PriorityTaskQueue()

        if validators is not None:
            self.validators.extend(validators)
            logger.debug("Validators initialized: %s", self.validators)

        self.task_runners: list[TaskRunner] = []
        if task_runners is not None:
            self.task_runners.extend(task_runners)
            logger.debug("Agents initialized: %s", self.task_runners)

        self.config = config

        self._validators_are_stale = True

        self.rcm = rcm

        if seed_tasks:
            for task in seed_tasks:
                # Seed tasks are assumed to be of the highest priority
                task.priority = 0
                self.priority_queue.push(task)
                logger.info("Seed task %s added to stack.", task)

        logger.info("TaskManager initialized.")

    def execute_task(self, task: Task) -> TaskResult:
        logger.info("Executing task: %s", task)
        agent = self.get_agent_for_task(task)
        logger.info("Agent selected for task: %s", agent)

        result: TaskResult
        try:
            result = agent.execute_task(self.rcm, task)
        except Exception as e:
            logger.error("Unhandled exception executing task %s: %e", task, e)
            result = TaskResult(encountered_errors=[str(e)], modified_files=[])

        logger.debug("Task execution result: %s", result)
        return result

    def get_agent_for_task(self, task: Task) -> TaskRunner:
        for agent in self.task_runners:
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
            logger.error("Encountered errors: %s", result.encountered_errors)

    def run_validators(self) -> list[Task]:
        logger.info("Running validators.")
        validation_tasks: list[Task] = []

        def run_validator(
            validator: ValidationStep,
        ) -> tuple[ValidationStep, Optional[ValidationResult]]:
            logger.debug("Running validator: %s", validator)
            try:
                result = validator.run()
                return validator, result
            except Exception as e:
                logger.error(
                    "Validator %s failed to execute with an unhandled error: %s",
                    validator,
                    e,
                )
                return validator, None

        with ThreadPoolExecutor() as executor:
            # Submit all validators to the executor
            future_to_validator = {
                executor.submit(run_validator, v): v for v in self.validators
            }

            # Process results as they complete
            for future in as_completed(future_to_validator):
                validator = future_to_validator[future]
                try:
                    validator, result = future.result()
                    if result is None:
                        continue  # Skip if the validator failed

                    logger.debug("Validator result: %s", result)
                    if not result.passed:
                        validation_tasks.extend(result.errors)
                        logger.info(
                            "Found %d tasks from validator %s",
                            len(result.errors),
                            validator,
                        )
                        logger.debug(
                            "Validator %s found errors: %s", validator, result.errors
                        )
                except Exception as e:
                    logger.error(
                        "Exception occurred while processing validator %s: %s",
                        validator,
                        e,
                    )

        self._validators_are_stale = False
        logger.info("Found %d tasks from validators", len(validation_tasks))
        logger.debug("Validators are up to date.")
        return validation_tasks

    def get_next_task(
        self,
        max_priority: Optional[int] = None,
        max_iterations: Optional[int] = None,
        max_depth: Optional[int] = None,
    ) -> Generator[Task, Any, None]:
        self.initialize_priority_queue()
        iterations = 0

        while self.priority_queue.has_tasks_within_depth(max_depth):
            if max_iterations is not None and iterations >= max_iterations:
                # kill the loop, no more iterations allowed
                return
            iterations += 1
            task = self.priority_queue.pop()
            if (
                max_priority is not None
                and task.oldest_ancestor().priority > max_priority
            ):
                # Put the task back and stop iteration
                self.priority_queue.push(task)
                return
            logger.debug("Popped task from stack: %s", task)
            if self.should_skip_task(task):
                logger.debug("Skipping task: %s", task)
                continue

            logger.info("Yielding task: %s", task)
            yield task
            # Once we yield the task, if we are at max_iterations we shouldn't re-run
            # validators.
            if max_iterations is not None and iterations >= max_iterations:
                # kill the loop, no more iterations allowed
                return
            self.handle_new_tasks_after_processing(task)

    def initialize_priority_queue(self) -> None:
        logger.info("Initializing task stacks.")

        new_tasks = self.run_validators()
        for task in new_tasks:
            if not self.should_skip_task(task):
                self.priority_queue.push(task)

    def handle_new_tasks_after_processing(self, task: Task) -> None:
        logger.info("Handling new tasks after processing task: %s", task)
        self._validators_are_stale = True
        unprocessed_new_tasks = set(self.run_validators())
        logger.debug("Unprocessed new tasks: %s", unprocessed_new_tasks)

        # Identify resolved tasks to remove from stacks
        tasks_in_queue = self.priority_queue.all_tasks()
        resolved_tasks = tasks_in_queue - unprocessed_new_tasks
        logger.debug("Resolved tasks to remove from stacks: %s", resolved_tasks)

        # Remove resolved tasks from the stacks and mark them as processed
        for resolved_task in resolved_tasks:
            self.priority_queue.remove(resolved_task)
            self.processed_tasks.add(resolved_task)
            logger.info(
                "Task %s resolved indirectly and removed from queue.", resolved_task
            )

        # Check if the current task is still unprocessed (or similar)
        similar_tasks = [
            t for t in unprocessed_new_tasks if self.is_similar_to_task(t, task)
        ]

        if similar_tasks:
            for t in similar_tasks:
                unprocessed_new_tasks.remove(t)
            logger.debug("Task %s still unsolved after execution.", task)
            self.handle_ignored_task(task)
        else:
            self.processed_tasks.add(task)
            logger.debug("Task %s processed successfully.", task)

        new_child_tasks = unprocessed_new_tasks - tasks_in_queue
        # We want the higher priority things at the end of the list, so when we append and pop we get the highest priority
        for child_task in sorted(new_child_tasks):
            try:
                if child_task == task:
                    raise ValueError(
                        f"A task cannot be added as a child of itself: {task}"
                    )
                child_task.parent = task
                child_task.depth = task.depth + 1
                task.children.append(child_task)
                if not self.should_skip_task(child_task):
                    self.priority_queue.push(child_task)
            except ValueError as e:
                logger.error(f"Error adding child task: {e}")

    def should_skip_task(self, task: Task) -> bool:
        skip = task in self.processed_tasks or task in self.ignored_tasks
        logger.debug("Should skip task %s: %s", task, skip)
        return skip

    def is_similar_to_task(self, task1: Task, task2: Optional[Task]) -> bool:
        if task2 is None:
            return False
        same = task2 == task1
        logger.debug("Task %s is same to prior task %s: %s", task1, task2, same)
        # TODO(fabianvf): Give tasks the ability to provide a specific fuzzy equals function?
        similar = False
        if hasattr(task1, "fuzzy_equals"):
            similar = task1.fuzzy_equals(task2, offset=2)
        logger.debug("Task %s is similar to prior task %s: %s", task1, task2, similar)
        return same or similar

    def handle_ignored_task(self, task: Task) -> None:
        logger.info("Handling ignored task: %s", task)
        task.retry_count += 1
        if task.retry_count < task.max_retries:
            logger.debug(
                "Task %s failed (retry count: %s), adding back to stack",
                task,
                task.retry_count,
            )
            self.priority_queue.push(task)
        else:
            self.ignored_tasks.append(task)
            logger.warning(
                "Task %s exceeded max retries and added to ignored tasks.", task
            )

    def stop(self) -> None:
        logger.info("Stopping TaskManager.")
        for a in self.task_runners:
            if hasattr(a, "stop"):
                a.stop()
                logger.debug("Stopped agent: %s", a)

        for v in self.validators:
            if hasattr(v, "stop"):
                v.stop()
                logger.debug("Stopped validator: %s", v)
