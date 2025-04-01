import subprocess
from io import StringIO
from pathlib import Path
from shutil import which
from typing import Literal

from langchain_core.messages import ToolMessage
from langgraph.graph import END
from langgraph.prebuilt.tool_node import InjectedState
from langgraph.types import Command
from lxml import etree as ET  # trunk-ignore(bandit/B410)
from typing_extensions import Annotated

from kai.constants import ENV
from kai.logging.logging import TRACE, get_logger
from kai.reactive_codeplanner.agentic.schemas.maven_compiler.schema import (
    Dependency,
    InitState,
)
from kai.reactive_codeplanner.agentic.tools.base import KaiBaseTool

logger = get_logger(__name__)


class GetAllAvailableDependencies(KaiBaseTool):

    def __init__(self) -> None:
        super().__init__(
            name="GetAllAvailableDependencies",
            description="When a pom file is present in dependency management section we need to get all the available dependnecies",
        )

    # Note that the command
    def _run(
        self, state: Annotated[InitState, InjectedState]
    ) -> Command[Literal["end", "agent"]]:
        """List all the dependencies available for the projct given by source directory"""
        deps: list[Dependency] = []

        tool_call_id = self.get_tool_id(state.messages)

        logger.log(
            TRACE, f"calling {self.__class__.__name__} tool with id: {tool_call_id}"
        )
        try:
            mavenPath = which("mvn") or "mvn"
            cmd = [mavenPath, "help:effective-pom"]
            #  trunk-ignore-begin(bandit/B603)
            path = Path(state.file_path).parent
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
                cwd=path,
                env=ENV,
            )
            logger.log(TRACE, "running maven process: %s", process)
            if process.returncode == 0:
                deps = self.parse_effective_pom(process.stdout)
            else:
                logger.info(
                    "unable to list all dependencies: %s -- %s",
                    process.returncode,
                    process.stdout,
                )
                return Command()
        except FileNotFoundError as e:
            logger.info("Maven is not installed or not found in the system PATH.")
            raise e
        except Exception as e:
            logger.info(f"unable to call tool - {e}")
            raise e
        state.dependencies = deps
        state.messages.append(
            ToolMessage(
                f"added {deps.__len__()} to the state", tool_call_id=tool_call_id
            )
        )
        return Command(update=state.model_dump(), goto=END)

    def parse_effective_pom(self, output: str) -> list[Dependency]:
        buffer = StringIO(output)
        xmlBuffer = StringIO("")
        for line in buffer.readlines():
            line = line.strip()
            if (
                "[INFO]" in line
                or "Effective POMs, after inheritance, interpolation, and profiles are applied:"
                in line
                or not line
            ):
                continue
            else:
                if 'encoding="UTF-8"' in line:
                    line = line.replace('encoding="UTF-8"', "")
                xmlBuffer.writelines(line)

        xmlBuffer.seek(0)
        tree = ET.parse(xmlBuffer)

        outputDeps: list[Dependency] = []
        for child in tree.iter():
            if "dependency" in child.tag and not "Management" in child.tag:
                outputDep = Dependency(artifact_id=None, group_id=None, version=None)
                for dep in child:
                    if "artifactId" in dep.tag and dep.text:
                        outputDep.artifact_id = dep.text
                    if "groupId" in dep.tag and dep.text:
                        outputDep.group_id = dep.text
                    if "version" in dep.tag and dep.text:
                        outputDep.version = dep.text
                if outputDep.is_valid():
                    outputDeps.append(outputDep)
                else:
                    print(
                        f"unable to get all info for dep: {child} - {dep}", child, dep
                    )
                    logger.info("unable to get all info for dep: %s - %s", child, dep)

        return outputDeps
