from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from kai.cache import CachePathResolver, TaskBasedPathResolver
from kai.reactive_codeplanner.task_manager.api import Task


@dataclass
class AgentRequest:
    file_path: Path
    task: Task
    background: Optional[str] = None
    cache_path_resolver: CachePathResolver = field(init=False)

    def __post_init__(self) -> None:
        self.cache_path_resolver = TaskBasedPathResolver(
            task=self.task, request_type=self.__class__.__name__.lower()
        )


@dataclass
class AgentResult:
    encountered_errors: list[str] | None = None
    # TODO: consider changing this, as an agent should not be responsible for changing the file
    # We may not need this generically, but for planning agents we may. leaving for now.
    file_to_modify: Path | None = None
    reasoning: str | None = None


class Agent(ABC):
    @abstractmethod
    def execute(self, ask: AgentRequest) -> AgentResult:
        """
        If the agent cannot handle the request, it should return an AgentResult
        with None values.
        """
