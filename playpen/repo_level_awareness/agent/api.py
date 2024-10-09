from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AgentRequest:
    file_path: str


@dataclass
class AgentResult:
    encountered_errors: list[str]
    modified_files: list[Path]


class Agent(ABC):
    @abstractmethod
    def execute(self, ask: AgentRequest) -> AgentResult:
        pass
