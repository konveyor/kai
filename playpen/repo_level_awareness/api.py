from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from .git_vfs import RepoContextManager


@dataclass
class RpcClientConfig:
    repo_directory: Path


# FIXME: Oh god oh no oh jeez oh man
class Task:
    pass


# FIXME: Might not need
@dataclass
class TaskResult:
    encountered_errors: list[str]
    modified_files: list[Path]


@dataclass
class ValidationError(Task):
    pass


@dataclass
class ValidationResult:
    passed: bool
    errors: list[ValidationError]


class ValidationStep(ABC):
    def __init__(self, RpcClientConfig: RpcClientConfig) -> None:
        self.config = RpcClientConfig

    @abstractmethod
    def run(self) -> ValidationResult:
        pass


class Agent(ABC):
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
