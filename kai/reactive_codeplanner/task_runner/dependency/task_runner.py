import os
from dataclasses import dataclass
from pathlib import Path

from lxml import etree as ET  # trunk-ignore(bandit/B410)
from opentelemetry import trace

from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.dependency_agent.dependency_agent import (
    MavenDependencyAgent,
    MavenDependencyRequest,
    MavenDependencyResult,
)
from kai.reactive_codeplanner.task_manager.api import Task, TaskResult
from kai.reactive_codeplanner.task_runner.api import TaskRunner
from kai.reactive_codeplanner.task_runner.compiler.maven_validator import (
    PackageDoesNotExistError,
)
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager

logger = get_logger(__name__)
tracer = trace.get_tracer("dependency_task_runner")


@dataclass
class DependencyTaskResponse:
    reasoning: str
    java_file: str
    additional_information: str


class DependencyTaskRunner(TaskRunner):
    """TODO: Add Class Documentation"""

    handled_type = (PackageDoesNotExistError,)

    def __init__(self, agent: MavenDependencyAgent) -> None:
        self._agent = agent

    async def can_handle_task(self, task: Task) -> bool:
        return isinstance(task, self.handled_type)

    @tracer.start_as_current_span("dependency_task_execute")
    async def execute_task(self, rcm: RepoContextManager, task: Task) -> TaskResult:
        if not isinstance(task, PackageDoesNotExistError):
            logger.error("Unexpected task type %r", task)
            return TaskResult(encountered_errors=[], modified_files=[], summary="")

        msg = f"Maven Compiler Error:\n{task.compiler_error_message()}"

        maven_dep_response = await self._agent.execute(
            MavenDependencyRequest(
                file_path=Path(task.file),
                task=task,
                message=msg,
                background=task.background(),
            )
        )
        logger.info("got mvn dep response: %r", maven_dep_response)

        if not isinstance(maven_dep_response, MavenDependencyResult):
            return TaskResult(encountered_errors=[], modified_files=[], summary="")

        if not maven_dep_response.final_answer:
            logger.info(
                "No final answer was given, we need to return with nothing modified. result: %r",
                maven_dep_response,
            )
            return TaskResult(
                encountered_errors=[
                    f"unable to fix compiler message: {msg} no dependency found"
                ],
                modified_files=[],
                summary="",
            )

        if not maven_dep_response.fqdn_response:
            logger.info(
                "we got a final answer, but it must have skipped steps in the LLM, we need to review the LLM call response %r",
                maven_dep_response,
            )
            return TaskResult(encountered_errors=[], modified_files=[], summary="")

        logger.debug(
            "we are now updating the pom based %s", maven_dep_response.final_answer
        )
        pom = os.path.join(os.path.join(rcm.project_root, "pom.xml"))
        tree = ET.parse(pom)  # trunk-ignore(bandit/B320)
        if tree is None:
            return TaskResult(modified_files=[], encountered_errors=[], summary="")
        root = tree.getroot()
        if root is None:
            return TaskResult(modified_files=[], encountered_errors=[], summary="")
        deps = root.find("{http://maven.apache.org/POM/4.0.0}dependencies")

        if deps is None or not isinstance(deps, ET._Element):
            return TaskResult(modified_files=[], encountered_errors=[], summary="")

        # deduplicate deps
        for dep in deps:
            if maven_dep_response.fqdn_response.match_dep(dep=dep):
                logger.debug("removing existing duplicate dep %s", dep)
                deps.remove(dep)

        ## We always need to add the new dep
        deps.append(maven_dep_response.fqdn_response.to_xml_element())

        if maven_dep_response.find_in_pom is not None:
            if maven_dep_response.find_in_pom.override:
                ## we know we need to remove this dep
                for dep in deps:
                    if maven_dep_response.find_in_pom.match_dep(dep):
                        logger.debug("found dep %r and removing", dep)
                        deps.remove(dep)

        # This fixes whitespace/indentations on the new dependencies
        ET.indent(tree)
        tree.write(file=pom, encoding="utf-8", pretty_print=True)
        rcm.commit(
            f"DependencyTaskRunner changed file {str(pom)}",
            None,
        )

        return TaskResult(modified_files=[Path(pom)], encountered_errors=[], summary="")

    async def refine_task(self, errors: list[str]) -> None:
        # Knows that it's the refine step so that it might not spawn as much
        # stuff.
        pass

    async def can_handle_error(self, errors: list[str]) -> bool:
        return False
