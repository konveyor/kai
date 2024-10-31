from typing import Optional

import kai.logging.logging as logging
from kai.reactive_codeplanner.task_manager.api import Task

logger = logging.get_logger(__name__)


class PriorityTaskQueue:

    def __init__(self) -> None:
        self.task_stacks: dict[int, list[Task]] = {}

    def push(self, task: Task) -> None:
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

    def pop(self) -> Task:
        highest_priority = min(self.task_stacks.keys())
        task_stack = self.task_stacks[highest_priority]
        task = task_stack.pop()
        logger.debug("Popped task %s from priority %s stack.", task, highest_priority)
        if not task_stack:
            del self.task_stacks[highest_priority]
            logger.debug("Priority %s stack is empty and removed.", highest_priority)
        return task

    def has_tasks_within_depth(self, max_depth: Optional[int]) -> bool:
        for task_stack in self.task_stacks.values():
            for task in task_stack:
                if max_depth is None or task.depth <= max_depth:
                    return True
        return False

    def remove(self, task: Task) -> None:
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

    def all_tasks(self) -> set[Task]:
        return set().union(*self.task_stacks.values())
