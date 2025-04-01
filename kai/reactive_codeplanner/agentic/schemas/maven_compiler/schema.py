from dataclasses import field
from pathlib import Path
from typing import Annotated, Optional

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import InjectedState
from pydantic import BaseModel, ConfigDict

from kai.cache import CachePathResolver
from kai.llm_interfacing.model_provider import ModelProvider
from kai.reactive_codeplanner.task_manager.api import Task


class Dependency(BaseModel):
    artifact_id: Optional[str]
    group_id: Optional[str]
    version: Optional[str]

    def is_valid(self) -> bool:
        if self.artifact_id is None or self.group_id is None or self.version is None:
            return False
        return True


class State(BaseModel):
    """Base state class"""

    messages: Annotated[list[AnyMessage], add_messages]


class InitState(State):
    """Initial state of the graph base model"""

    # Init Fields
    file_path: Path
    task: Task
    background: str
    dependencies: list[Dependency]
