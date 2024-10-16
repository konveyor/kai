# trunk-ignore-begin(ruff/E402)
import sys

sys.modules["_elementtree"] = None  # type: ignore[assignment]
import json

# trunk-ignore(bandit/B405)
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from langchain_core.messages import HumanMessage

# trunk-ignore-end(ruff/E402)


@dataclass
class FQDNResponse:
    artifact_id: str
    group_id: str
    version: str

    def to_llm_message(self) -> HumanMessage:
        return HumanMessage(f"the result is {json.dumps(self.__dict__)}")

    def to_xml_element(self) -> ET.Element:
        parent = ET.Element("{http://maven.apache.org/POM/4.0.0}dependency")
        artifact = ET.Element("{http://maven.apache.org/POM/4.0.0}artifactId")
        artifact.text = self.artifact_id
        group = ET.Element("{http://maven.apache.org/POM/4.0.0}groupId")
        group.text = self.group_id
        version = ET.Element("{http://maven.apache.org/POM/4.0.0}version")
        version.text = self.version
        parent.append(artifact)
        parent.append(group)
        parent.append(version)
        return parent


@dataclass
class FindInPomResponse:
    start_line: int
    end_line: int

    def to_llm_message(self) -> HumanMessage:
        return HumanMessage(
            f"the start_line is {self.start_line} and end_line is {self.end_line}"
        )
