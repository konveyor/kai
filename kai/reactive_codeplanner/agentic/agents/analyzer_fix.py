import os
from dataclasses import dataclass
from pathlib import Path

from langgraph.graph import StateGraph

from kai.analyzer_types import Incident
from kai.llm_interfacing.model_provider import ModelProvider
from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agentic.agents.analyzer_fix import guess_language
from kai.reactive_codeplanner.agentic.api import Agent, AgentRequest, AgentResult
from kai.reactive_codeplanner.agentic.schemas.analyzer_fix.analyzer_fix import (
    AnalysisAgentState,
)
from kai.rpc_server.chat import get_chatter_contextvar

logger = get_logger(__name__)
chatter = get_chatter_contextvar()


@dataclass
class AnalyzerFixRequest(AgentRequest):
    file_content: str
    incidents: list[Incident]
    sources: list[str]
    targets: list[str]


@dataclass
class AnalyzerFixResponse(AgentResult):
    updated_file_content: str | None = None
    additional_information: str | None = None
    reasoning: str | None = None


class AnalyzerAgent(Agent):
    def __init__(
        self,
        model_provider: ModelProvider,
        retries: int = 1,
    ) -> None:
        self._model_provider = model_provider
        self._retries = retries

    async def execute(self, ask: AgentRequest) -> AnalyzerFixResponse:
        await chatter.get().chat_simple("AnalyzerAgent executing...")

        if not isinstance(ask, AnalyzerFixRequest):
            return AnalyzerFixResponse(
                encountered_errors=["invalid request type"],
                file_to_modify=None,
                reasoning=None,
                additional_information=None,
                updated_file_content=None,
            )

        return AnalyzerFixResponse(
            encountered_errors=[],
            file_to_modify=Path(os.path.abspath(ask.file_path)),
            reasoning="",
            additional_information="",
            updated_file_content="",
        )

    def _agent_graph_v1(self, ask: AnalyzerFixRequest) -> StateGraph:
        guess_language(ask.file_content, ask.file_path.name)

        StateGraph(AnalysisAgentState())
