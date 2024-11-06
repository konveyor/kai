from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AgentRequest:
    file_path: Path


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
