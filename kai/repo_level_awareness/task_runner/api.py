from abc import ABC, abstractmethod

from kai.repo_level_awareness.api import Task, TaskResult
from kai.repo_level_awareness.vfs.git_vfs import RepoContextManager


class TaskRunner(ABC):
    @abstractmethod
    def can_handle_task(self, task: Task) -> bool:
        pass

    @abstractmethod
    def execute_task(self, rcm: RepoContextManager, task: Task) -> TaskResult:
        pass

    @abstractmethod
    def refine_task(self, errors: list[str]) -> None:
        # Knows that it's the refine step so that it might not spawn as much
        # stuff.
        pass

    @abstractmethod
    def can_handle_error(self, errors: list[str]) -> bool:
        pass
