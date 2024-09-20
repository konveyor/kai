from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator, Iterator, Optional

from pydantic import BaseModel


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

    def run(self) -> ValidationResult:
        pass


class Agent(ABC):
    def can_handle_task(self, task: Task) -> bool:
        pass

    def execute_task(self, task: Task) -> TaskResult:
        pass

    def refine_task(self, errors: list[str]) -> None:
        # Knows that it's the refine step so that it might not spawn as much
        # stuff.
        pass

    def can_handle_error(self, errors: list[str]) -> bool:
        pass
