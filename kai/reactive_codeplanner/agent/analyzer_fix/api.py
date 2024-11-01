from dataclasses import dataclass

from kai.analyzer_types import Incident
from kai.reactive_codeplanner.agent.api import AgentRequest, AgentResult


@dataclass
class AnalyzerFixRequest(AgentRequest):
    file_content: str
    incidents: list[Incident]


@dataclass
class AnalyzerFixResponse(AgentResult):
    updated_file_content: str | None = None
    additional_information: str | None = None
