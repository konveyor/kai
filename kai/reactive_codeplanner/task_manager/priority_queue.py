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

        priority = task.oldest_ancestor().priority
        if priority not in self.task_stacks:
            self.task_stacks[priority] = []
            logger.debug("Created new task stack for priority %s.", priority)
        self.task_stacks[priority].append(task)
        self.task_stacks[priority].sort(reverse=True)
        logger.debug("Task %s added to priority %s stack.", task, priority)

    def pop(self, max_depth: Optional[int] = None) -> Task:
        for priority in sorted(self.task_stacks.keys()):
            task_stack = self.task_stacks[priority]
            if self._stack_has_tasks_within_depth(task_stack, max_depth):
                task = self._pop_task_within_depth(task_stack, max_depth)
                logger.debug(
                    "Popped task %s from priority %s stack with max_depth %s.",
                    task,
                    priority,
                    max_depth,
                )
                if not task_stack:
                    del self.task_stacks[priority]
                    logger.debug("Priority %s stack is empty and removed.", priority)
                return task
        if max_depth is not None:
            raise IndexError(
                f"No tasks available within the specified max_depth of {max_depth}"
            )
        raise IndexError("Pop from empty PriorityTaskQueue")

    def _pop_task_within_depth(
        self, task_stack: list[Task], max_depth: Optional[int]
    ) -> Task:
        for idx in reversed(range(len(task_stack))):
            task = task_stack[idx]
            if max_depth is None or task.depth <= max_depth:
                return task_stack.pop(idx)
        raise IndexError(
            f"No tasks in the stack meet the depth requirement of {max_depth}"
        )

    def has_tasks_within_depth(self, max_depth: Optional[int]) -> bool:
        if max_depth is None:
            return len(self.all_tasks()) > 0
        return any(
            [
                self._stack_has_tasks_within_depth(s, max_depth)
                for s in self.task_stacks.values()
            ]
        )

    def _stack_has_tasks_within_depth(
        self, stack: list[Task], depth: Optional[int]
    ) -> bool:
        if depth is None:
            return len(stack) > 0
        return any([task.depth <= depth for task in stack])

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

    def __str__(self) -> str:
        queue_tasks_set = self.all_tasks()
        top_level_tasks = set(task.oldest_ancestor() for task in queue_tasks_set)
        visited: set[Task] = set()

        lines = []
        for task in top_level_tasks:
            lines.extend(
                self._stringify_tasks(
                    task,
                    indent=0,
                    visited=visited,
                    queue_tasks_set=queue_tasks_set,
                )
            )
        return "\n".join(lines)

    def _stringify_tasks(
        self,
        task: Task,
        indent: int,
        visited: set[Task],
        queue_tasks_set: set[Task],
    ) -> list[str]:
        lines = []
        if task in visited:
            logger.debug(
                "%s%s(...)  # Already printed",
                "  " * indent,
                task.__class__.__name__,
            )
            return []
        visited.add(task)

        if task in queue_tasks_set:
            status = ""
        elif task.retry_count == task.max_retries:
            status = "Ignored: "
        else:
            status = "Solved: "

        prefix = ""
        if task.depth > 0:
            prefix = "|" + "-" * indent

        lines.append(
            f"{prefix}{status}{task}(priority={task.priority}, depth={task.depth}, retries={task.retry_count})"
        )

        for child in task.children:
            lines.extend(
                self._stringify_tasks(
                    child,
                    indent=indent + 1,
                    visited=visited,
                    queue_tasks_set=queue_tasks_set,
                )
            )
        return lines
