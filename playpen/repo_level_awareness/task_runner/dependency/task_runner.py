# trunk-ignore-begin(ruff/E402)
import sys

sys.modules["_elementtree"] = None
import logging
import os
import xml.etree.ElementTree as ET  # trunk-ignore(bandit/B405)
from dataclasses import dataclass
from pathlib import Path

from playpen.repo_level_awareness.agent.dependency_agent.dependency_agent import (
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
from playpen.repo_level_awareness.utils.xml import LineNumberingParser
from playpen.repo_level_awareness.vfs.git_vfs import RepoContextManager

# trunk-ignore-end(ruff/E402)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        msg = task.message
        if isinstance(task, PackageDoesNotExistError):
            msg = f"Maven Compiler Error:\n{task.message}"

        r = self._agent.execute(MavenDependencyRequest(task.file, msg))

        if not r.final_answer:
            logger.info(
                "No final answer was given, we need to return with nothing modified. result: %r",
                r,
            )
            return TaskResult(encountered_errors=[], modified_files=[])

        if not r.fqdn_response or not r.find_in_pom:
            logger.info(
                "we got a final answer, but it must have skipped steps in the LLM, we need to review the LLM call resposne %r",
                r,
            )
            return TaskResult(encountered_errors=[], modified_files=[])

        logger.debug("we are now updating the pom based %s", r.final_answer)
        pom = os.path.join(os.path.join(rcm.project_root, "pom.xml"))
        # Needed to remove ns0:
        ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
        tree = ET.parse(pom, LineNumberingParser())  # trunk-ignore(bandit/B314)
        root = tree.getroot()
        deps = root.find("{http://maven.apache.org/POM/4.0.0}dependencies")

        ## We always need to add the new dep
        deps.append(r.fqdn_response.to_xml_element())

        if deps._start_line_number != r.find_in_pom.start_line:
            ## we know we need to remove this dep
            for dep in deps:
                if (
                    dep._start_line_number == r.find_in_pom.start_line
                    and dep._end_line_number == r.find_in_pom.end_line
                ):
                    logger.debug("found dep %r and removing", dep)
                    deps.remove(dep)

        with open(pom, "w") as p:
            ET.indent(tree, "\t", 0)
            pretty_xml = ET.tostring(root, encoding="UTF-8", default_namespace="")
            p.write(pretty_xml.decode("utf-8"))
            rcm.commit("dependnecy", r)

        return TaskResult(modified_files=[Path(pom)], encountered_errors=[])

    def refine_task(self, errors: list[str]) -> None:
        # Knows that it's the refine step so that it might not spawn as much
        # stuff.
        pass

    def can_handle_error(self, errors: list[str]) -> bool:
        pass
