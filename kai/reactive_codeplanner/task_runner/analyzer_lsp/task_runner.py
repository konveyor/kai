from pathlib import Path

from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.analyzer_fix.agent import AnalyzerAgent
from kai.reactive_codeplanner.agent.analyzer_fix.api import (
    AnalyzerFixRequest,
    AnalyzerFixResponse,
)
from kai.reactive_codeplanner.task_manager.api import Task, TaskResult
from kai.reactive_codeplanner.task_runner.analyzer_lsp.api import AnalyzerRuleViolation
from kai.reactive_codeplanner.task_runner.api import TaskRunner
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager

logger = get_logger(__name__)


class AnalyzerTaskRunner(TaskRunner):
    """This agent is reponsible for taking a given Incident and determining a fix for that incident.

    For a given file it will asking LLM's for the changes that are needed for the at whole file
    returning the results.
    """

    def __init__(self, agent: AnalyzerAgent) -> None:
        self.agent = agent

    def refine_task(self, errors: list[str]) -> None:
        """We currently do not refine the tasks"""
        raise NotImplementedError("We currently do not refine the tasks")

    def can_handle_error(self, errors: list[str]) -> bool:
        """We currently do not know if we can handle errors"""
        raise NotImplementedError("We currently do not know if we can handle errors")

    def can_handle_task(self, task: Task) -> bool:
        """Will determine if the task if a MavenCompilerError, and if we can handle these issues."""
        return isinstance(task, AnalyzerRuleViolation)

    def execute_task(self, rcm: RepoContextManager, task: Task) -> TaskResult:
        """This will be responsible for getting the full file from LLM and updating the file on disk"""

        # convert the task to the MavenCompilerError
        if not isinstance(task, AnalyzerRuleViolation):
            return TaskResult(encountered_errors=[], modified_files=[])

        with open(task.file) as f:
            src_file_contents = f.read()

        agent_request = AnalyzerFixRequest(
            file_path=Path(task.file),
            file_content=src_file_contents,
            incidents=[task.incident],
        )
        result = self.agent.execute(agent_request)

        if not result or not isinstance(result, AnalyzerFixResponse):
            return TaskResult(
                encountered_errors=["response from agent was invalid"],
                modified_files=[],
            )

        if result.file_to_modify is None:
            return TaskResult(
                encountered_errors=["file to modify was not returned"],
                modified_files=[],
            )

        # rewrite the file, based on the java file returned
        if result.updated_file_content:
            with open(result.file_to_modify, "w") as f:
                f.write(result.updated_file_content)

            rcm.commit(f"AnalyzerTaskRunner changed file {str(task.file)}", None)
            return TaskResult(
                modified_files=[result.file_to_modify], encountered_errors=[]
            )

        return TaskResult(modified_files=[], encountered_errors=[])
