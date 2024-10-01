from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AgentTask:
    pass


@dataclass
class AgentTaskResult:
    encountered_errors: list[str]
    modified_files: list[Path]


class Agent(ABC):
    @abstractmethod
    def execute(self, ask: AgentTask) -> AgentTaskResult:
        pass
