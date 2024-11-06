import json
from dataclasses import dataclass

from langchain_core.messages import HumanMessage
from lxml import etree as ET  # trunk-ignore(bandit/B410)

MAVEN_DEPENDENCY_XML_KEY = "{http://maven.apache.org/POM/4.0.0}dependency"
MAVEN_ARTIFACT_ID_XML_KEY = "{http://maven.apache.org/POM/4.0.0}artifactId"
MAVEN_GROUP_ID_XML_KEY = "{http://maven.apache.org/POM/4.0.0}groupId"
MAVEN_VERSION_XML_KEY = "{http://maven.apache.org/POM/4.0.0}version"


@dataclass
class FQDNResponse:
    artifact_id: str
    group_id: str
    version: str

    def to_llm_message(self) -> HumanMessage:
        return HumanMessage(f"the result is {json.dumps(self.__dict__)}")

    def to_xml_element(self) -> ET._Element:
        parent = ET.Element(MAVEN_DEPENDENCY_XML_KEY)
        artifact = ET.Element(MAVEN_ARTIFACT_ID_XML_KEY)
        artifact.text = self.artifact_id
        group = ET.Element(MAVEN_GROUP_ID_XML_KEY)
        group.text = self.group_id
        version = ET.Element(MAVEN_VERSION_XML_KEY)
        version.text = self.version
        parent.append(artifact)
        parent.append(group)
        parent.append(version)
        return parent


@dataclass
class FindInPomResponse:
    override: bool
    group_id: str | None = None
    artifact_id: str | None = None
    version: str | None = None

    def to_llm_message(self) -> HumanMessage:
        return HumanMessage(
            ## TODO: I don't think that this will work.
            "the start_line is 1 and end_line is 2"
        )

    def match_dep(self, dep: ET._Element) -> bool:
        found = []
        for child in dep:
            if child.text in [self.group_id, self.artifact_id, self.version]:
                found.append(True)

        if len(found) == 3:
            return True
        return False
