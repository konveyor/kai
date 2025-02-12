#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Generator, Optional

from opentelemetry import trace

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
from kai.rpc_server.chat import get_chatter_contextvar

logger = logging.get_logger(__name__)
tracer = trace.get_tracer("task_manager")
chatter = get_chatter_contextvar()


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
        self._stale_validated_files: list[Path] = []

        self.rcm = rcm

        if seed_tasks:
            self.set_seed_tasks(*seed_tasks)

        logger.info("TaskManager initialized.")

    def set_seed_tasks(self, *tasks: Task) -> None:
        # Clear ignored/processed tasks, assuming the user is going to want
        # to resolve any issues found even if they've been seen before
        self.processed_tasks = set()
        self.ignored_tasks = list()

        # Clear existing seed tasks
        existing_tasks = self.priority_queue.task_stacks.get(0, [])
        for task in existing_tasks:
            self.priority_queue.remove(task)
            # Reset priority to default
            if task.parent:
                ancestor = task.oldest_ancestor()
                ancestor.priority = ancestor.__class__.priority
            else:
                task.priority = task.__class__.priority
            # Now add them back to the queue so they aren't mistakenly detected as children
            self.priority_queue.push(task)

        msg = "<details><summary>Got some pending tasks</summary>"
        msg += f"<ul>{''.join(f'<li>{str(t)}</li>' for t in tasks)}</ul>"
        msg += "</details>"
        chatter.get().chat_markdown(msg)

        for task in tasks:
            task.priority = 0
            self.priority_queue.push(task)
            logger.info("Seed task %s added to stack.", task)

    def execute_task(self, task: Task) -> TaskResult:
        logger.info("Executing task: %s", task)
        agent = self.get_agent_for_task(task)
        logger.info("Agent selected for task: %s", agent)

        chatter.get().chat_simple(
            f"Using agent {str(agent.__class__.__name__)} to execute task {str(task)}"
        )

        result: TaskResult
        try:
            result = agent.execute_task(self.rcm, task)
        except Exception as e:
            logger.exception("Unhandled exception executing task %s", task)
            chatter.get().chat_simple(f"Unhandled exception executing task {str(task)}")
            result = TaskResult(
                encountered_errors=[str(e)], modified_files=[], summary=""
            )

        logger.debug("Task execution result: %s", result)
        task.result = result
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
            self._stale_validated_files.append(file_path)
            if file_path not in self.unprocessed_files:
                self.unprocessed_files.append(file_path)
                self._validators_are_stale = True
                logger.debug("File %s marked as unprocessed.", file_path)

        if len(result.encountered_errors) > 0:
            logger.error("Encountered errors: %s", result.encountered_errors)

    def run_validators(self) -> list[Task]:
        logger.info("Running validators.")
        chatter.get().chat_simple("Running validators.")

        validation_tasks: list[Task] = []

        @tracer.start_as_current_span("run_validator")
        def run_validator(
            validator: ValidationStep,
        ) -> tuple[ValidationStep, Optional[ValidationResult]]:
            logger.debug(f"Running validator: {str(validator)}")
            chatter.get().chat_simple(f"Running validator {str(validator)}")

            try:
                scoped_paths: Optional[list[Path]] = None
                if len(self._stale_validated_files) > 0:
                    scoped_paths = self._stale_validated_files
                result = validator.run(scoped_paths=scoped_paths)
                return validator, result
            except Exception as e:
                logger.exception(
                    f"Validator {str(validator)} failed to execute with an unhandled error:"
                )
                chatter.get().chat_simple(
                    f"Validator {str(validator)} failed to execute with an unhandled error: {str(e)}"
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

                        msg = "<details>"
                        msg += f"<summary>Found {len(result.errors)} tasks from validator {str(validator)}</summary>"
                        msg += "<ul>"
                        for e in result.errors:
                            msg += f"<li>{e}</li>"
                        msg += "</ul></details>"
                        chatter.get().chat_markdown(msg)

                except Exception:
                    logger.exception(
                        "Exception occurred while processing validator %s:", validator
                    )

        self._stale_validated_files = []
        self._validators_are_stale = False
        logger.info("Found %d tasks from validators", len(validation_tasks))
        logger.debug("Validators are up to date.")
        return validation_tasks

    @tracer.start_as_current_span("get_next_task")
    def get_next_task(
        self,
        max_priority: Optional[int] = None,
        max_depth: Optional[int] = None,
    ) -> Generator[Task, Any, None]:
        # If we're being run at depth 0 and seed tasks have been set, don't bother running validators
        seed_tasks_only = max_depth == 0 and self.priority_queue.has_tasks_within_depth(
            0
        )
        if not seed_tasks_only:
            self.initialize_priority_queue()

        while self.priority_queue.has_tasks_within_depth(max_depth):
            task = self.priority_queue.pop(max_depth=max_depth)
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
            # If our depth is 0, we won't follow up on issues anyway
            # We do lose the ability to verify a solution worked, so
            # TODO(@fabianvf) we may have to adjust that at some point
            if max_depth == 0:
                self.handle_depth_0_task_after_processing(task)
            else:
                self.handle_new_tasks_after_processing(task)

    def initialize_priority_queue(self) -> None:
        logger.info("Initializing task stacks.")

        # When we re-initialize the priority queue we need to start fresh
        # Assume that something has changed in the project and we need
        # to re-create the priority queue
        self._stale_validated_files = []
        new_tasks = self.run_validators()
        for task in new_tasks:
            if not self.should_skip_task(task):
                self.priority_queue.push(task)

    def handle_depth_0_task_after_processing(self, task: Task) -> None:
        logger.info(
            "Handling depth 0 task, assuming fix has applied for task: %s", task
        )
        self.priority_queue.remove(task)

    def handle_new_tasks_after_processing(self, task: Task) -> None:
        logger.info("Handling new tasks after processing task: %s", task)
        self._validators_are_stale = True
        unprocessed_new_tasks = set(self.run_validators())
        logger.debug("Unprocessed new tasks: %s", unprocessed_new_tasks)

        # Identify resolved tasks to remove from stacks
        tasks_in_queue = self.priority_queue.all_tasks()
        resolved_tasks = tasks_in_queue - unprocessed_new_tasks
        logger.debug("Resolved tasks to remove from stacks: %s", resolved_tasks)

        similar_non_resolved_tasks = set()

        for t in resolved_tasks:
            for u in unprocessed_new_tasks:
                if self.is_similar_to_task(t, u):
                    logger.debug("adding task to similar_non_resolved_task: %s", t)
                    similar_non_resolved_tasks.add(t)

        if similar_non_resolved_tasks:
            for t in similar_non_resolved_tasks:
                resolved_tasks.remove(t)

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
            except ValueError:
                logger.exception("Error adding child task")

    def should_skip_task(self, task: Task) -> bool:
        skip = task in self.processed_tasks or task in self.ignored_tasks
        logger.log(logging.TRACE, "Should skip task %s: %s", task, skip)
        return skip

    def is_similar_to_task(self, task1: Task, task2: Optional[Task]) -> bool:
        if task2 is None:
            return False
        same = task2 == task1
        if same:
            logger.log(
                logging.TRACE,
                "Task %s is same to prior task %s: %s",
                task1,
                task2,
                same,
            )
            return same
        # TODO(fabianvf): Give tasks the ability to provide a specific fuzzy equals function?
        similar = False
        if hasattr(task1, "fuzzy_equals"):
            similar = task1.fuzzy_equals(task2, offset=2)
            if similar:
                logger.log(
                    logging.TRACE,
                    "Task %s is similar to prior task %s: %s",
                    task1,
                    task2,
                    similar,
                )
                return similar
        return False

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
