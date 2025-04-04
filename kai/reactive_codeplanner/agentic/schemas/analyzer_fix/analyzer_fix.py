from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from kai.analyzer_types import Incident


class AnalysisAgentInputState(BaseModel):
    input_file_path: Path
    input_file_content: str
    language: str
    incidents: list[Incident]
    sources: list[str]
    targets: list[str]


class AnalysisFixNodeOutputState(BaseModel):
    additional_information: Optional[str] = None
    updated_input_file: Optional[str] = None
    reasoning: Optional[str] = None


class AdditionalInformationNodeOutputState(BaseModel):
    done: Optional[bool] = None


class AnalysisAgentState(
    AnalysisAgentInputState,
    AnalysisFixNodeOutputState,
    AdditionalInformationNodeOutputState,
):
    modified_files: list[str] = Field(default_factory=list)
