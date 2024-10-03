from dataclasses import dataclass
from typing import Optional

from playpen.repo_level_awareness.agent.api import AgentRequest
from playpen.repo_level_awareness.agent.dependency_agent import (
    MavenDependencyAgent,
    MavenDependencyRequest,
)
from playpen.repo_level_awareness.api import Task, TaskResult
from playpen.repo_level_awareness.task_runner.api import TaskRunner
from playpen.repo_level_awareness.task_runner.compiler.maven_validator import (
    PackageDoesNotExistError,
    SymbolNotFoundError,
)
from playpen.repo_level_awareness.task_runner.dependency.api import (
    DependencyValidationError,
)
from playpen.repo_level_awareness.vfs.git_vfs import RepoContextManager


@dataclass
class DependencyTaskResponse:
    reasoning: str
    java_file: str
    addional_information: str


class DependencyTaskRunner(TaskRunner):
    """TODO: Add Class Documentation"""

    handeled_type = (
        DependencyValidationError,
        SymbolNotFoundError,
        PackageDoesNotExistError,
    )

    def __init__(self, agent: MavenDependencyAgent) -> None:
        self._agent = agent

    def can_handle_task(self, task: Task) -> bool:
        return isinstance(task, self.handeled_type)

    def execute_task(self, rcm: RepoContextManager, task: Task) -> TaskResult:
        response: Optional[DependencyTaskResponse] = None
        if isinstance(task, PackageDoesNotExistError):
            p: PackageDoesNotExistError = task
            msg = f"Maven Compiler Error:\n{task.message}"
            response = self._agent.execute(MavenDependencyRequest(task.file, msg))

        response = self._agent.execute(MavenDependencyRequest(task.file, task.message))
        print(response)
        return TaskResult(encountered_errors=[], modified_files=[])

    def refine_task(self, errors: list[str]) -> None:
        # Knows that it's the refine step so that it might not spawn as much
        # stuff.
        pass

    def can_handle_error(self, errors: list[str]) -> bool:
        pass
