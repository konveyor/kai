from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AgentRequest:
    file_path: str


@dataclass
class AgentResult:
    encountered_errors: list[str] | None
    modified_files: list[Path] | None


class Agent(ABC):
    @abstractmethod
    def execute(self, ask: AgentRequest) -> AgentResult:
        """
        If the agent cannot handle the request, it should return an AgentResult
        with None values.
        """
        ...
