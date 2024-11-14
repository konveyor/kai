from dataclasses import dataclass
from typing import Optional

from kai.reactive_codeplanner.agent.api import AgentRequest, AgentResult
from kai.reactive_codeplanner.agent.reflection_agent import ReflectionTask
from kai.reactive_codeplanner.task_manager.api import Task
from kai.reactive_codeplanner.vfs.git_vfs import SpawningResult


@dataclass
class MavenCompilerAgentRequest(AgentRequest):
    file_contents: str
    line_number: int
    message: str


@dataclass
class MavenCompilerAgentResult(AgentResult, SpawningResult):
    updated_file_contents: str | None = None
    additional_information: str | None = None
    original_file: str | None = None
    message: str | None = None
    task: Task | None = None

    def to_reflection_task(self) -> Optional[ReflectionTask]:

        if (
            self.updated_file_contents is None
            or self.additional_information is None
            or self.original_file is None
            or self.message is None
            or self.file_to_modify is None
            or self.reasoning is None
            or self.task is None
        ):
            return None

        return ReflectionTask(
            file_path=self.file_to_modify,
            issues=[self.message],
            reasoning=self.reasoning,
            updated_file_contents=self.updated_file_contents,
            original_file_contents=self.original_file,
            task=self.task,
            background="",
        )
