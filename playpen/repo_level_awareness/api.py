from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from .git_vfs import RepoContextManager


@dataclass
class RpcClientConfig:
    repo_directory: Path


@dataclass
class Task:
    pass


# FIXME: Might not need
@dataclass
class TaskResult:
    encountered_errors: list[str]
    modified_files: list[Path]


@dataclass
class ValidationError(Task):
    file: str
    line: int
    column: int
    message: str


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


def fuzzy_equals(
    error1: ValidationError, error2: ValidationError, offset: int = 1
) -> bool:
    """
    Determines if two ValidationError objects are likely the same error,
    with a fuzzy comparison allowing for a line number offset.

    Args:
    - error1 (ValidationError): First error to compare.
    - error2 (ValidationError): Second error to compare.
    - offset (int): The allowed difference in line numbers for errors to still be considered the same.

    Returns:
    - bool: True if the errors are likely the same, False otherwise.
    """
    return (
        error1.file == error2.file
        and abs(error1.line - error2.line) <= offset
        and error1.column == error2.column
        and error1.message == error2.message
    )
