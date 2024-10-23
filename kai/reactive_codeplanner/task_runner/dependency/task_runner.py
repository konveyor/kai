# trunk-ignore-begin(ruff/E402)
import sys

sys.modules["_elementtree"] = None  # type: ignore[assignment]
import logging
import os
import xml.etree.ElementTree as ET  # trunk-ignore(bandit/B405)
from dataclasses import dataclass
from pathlib import Path

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
    SymbolNotFoundError,
)
from kai.reactive_codeplanner.task_runner.dependency.api import (
    DependencyValidationError,
)
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager
from kai.reactive_codeplanner.xml_helpers import LineNumberingParser

# trunk-ignore-end(ruff/E402)

logger = get_logger(__name__)


@dataclass
class DependencyTaskResponse:
    reasoning: str
    java_file: str
    additional_information: str


class DependencyTaskRunner(TaskRunner):
    """TODO: Add Class Documentation"""

    handled_type = (
        DependencyValidationError,
        SymbolNotFoundError,
        PackageDoesNotExistError,
    )

    def __init__(self, agent: MavenDependencyAgent) -> None:
        self._agent = agent

    def can_handle_task(self, task: Task) -> bool:
        return isinstance(task, self.handled_type)

    def execute_task(self, rcm: RepoContextManager, task: Task) -> TaskResult:
        if not isinstance(
            task,
            (DependencyTaskResponse, SymbolNotFoundError, PackageDoesNotExistError),
        ):
            logger.error("Unexpected task type %r", task)
            return TaskResult(encountered_errors=[], modified_files=[])

        msg = task.message
        if isinstance(task, PackageDoesNotExistError):
            msg = f"Maven Compiler Error:\n{task.message}"

        maven_dep_response = self._agent.execute(MavenDependencyRequest(task.file, msg))
        logger.info("got mvn dep response: %r", maven_dep_response)

        if not isinstance(maven_dep_response, MavenDependencyResult):
            return TaskResult(encountered_errors=[], modified_files=[])

        if not maven_dep_response.final_answer:
            logger.info(
                "No final answer was given, we need to return with nothing modified. result: %r",
                maven_dep_response,
            )
            return TaskResult(encountered_errors=[], modified_files=[])

        if not maven_dep_response.fqdn_response or not maven_dep_response.find_in_pom:
            logger.info(
                "we got a final answer, but it must have skipped steps in the LLM, we need to review the LLM call resposne %r",
                maven_dep_response,
            )
            return TaskResult(encountered_errors=[], modified_files=[])

        logger.debug(
            "we are now updating the pom based %s", maven_dep_response.final_answer
        )
        pom = os.path.join(os.path.join(rcm.project_root, "pom.xml"))
        # Needed to remove ns0:
        ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
        tree = ET.parse(pom, LineNumberingParser())  # trunk-ignore(bandit/B314)
        root = tree.getroot()
        deps = root.find("{http://maven.apache.org/POM/4.0.0}dependencies")

        if deps is None or not isinstance(deps, ET.Element):
            return TaskResult(modified_files=[], encountered_errors=[])

        ## We always need to add the new dep
        deps.append(maven_dep_response.fqdn_response.to_xml_element())

        if deps._start_line_number != maven_dep_response.find_in_pom.start_line:  # type: ignore[attr-defined]
            ## we know we need to remove this dep
            for dep in deps:
                if (
                    dep._start_line_number == maven_dep_response.find_in_pom.start_line  # type: ignore[attr-defined]
                    and dep._end_line_number == maven_dep_response.find_in_pom.end_line  # type: ignore[attr-defined]
                ):
                    logger.debug("found dep %r and removing", dep)
                    deps.remove(dep)

        with open(pom, "w") as p:
            ET.indent(tree, "\t", 0)
            pretty_xml = ET.tostring(root, encoding="UTF-8", default_namespace="")
            p.write(pretty_xml.decode("utf-8"))
            rcm.commit(
                f"DependencyTaskRunner changed file {str(pom)}",
                None,
            )

        return TaskResult(modified_files=[Path(pom)], encountered_errors=[])

    def refine_task(self, errors: list[str]) -> None:
        # Knows that it's the refine step so that it might not spawn as much
        # stuff.
        pass

    def can_handle_error(self, errors: list[str]) -> bool:
        return False
