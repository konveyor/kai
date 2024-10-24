# trunk-ignore-begin(ruff/E402)
import importlib
import sys
import xml.etree.ElementTree as ET  # trunk-ignore(bandit/B405)

# Forcing the reload after changing and re-importing will allow us
# to pass the test.
sys.modules["_elementtree"] = None  # type: ignore[assignment]
importlib.reload(ET)

import os
import unittest
import xml.etree.ElementTree as ET  # trunk-ignore(bandit/B405)
from dataclasses import dataclass
from pathlib import Path

from kai.reactive_codeplanner.agent.dependency_agent.api import (
    FindInPomResponse,
    FQDNResponse,
)
from kai.reactive_codeplanner.agent.dependency_agent.dependency_agent import (
    MavenDependencyAgent,
    _action,
    _llm_response,
    find_in_pom,
    search_fqdn,
)
from kai.reactive_codeplanner.agent.dependency_agent.util import (
    get_maven_query_from_code,
)

# trunk-ignore-end(ruff/E402)


class TestDependencyAgent(unittest.TestCase):

    def test_parse_llm_response_one_thought(self):
        content = """
Thought: The error message indicates that the dependency `org.apache.maven.shared:maven-filtering` is missing. I need to find the current version of this dependency in the `pom.xml` file and update it to the latest version.

Action:
```python
result = search_fqdn.run(artifact_id="maven-filtering", group_id="org.apache.maven.shared")
start_line, end_line = find_in_pom._run(relative_file_path="pom.xml", keywords={"groupId": "org.apache.maven.shared", "artifactId": "maven-filtering"})
xml = f"<dependency><groupId>{result.groupId}</groupId><artifactId>{result.artifactId}</artifactId><version>{result.version}</version></dependency>"
result = editor._run(relative_file_path="pom.xml", start_line=start_line, end_line=end_line, patch=xml)
```
Observation:
The action searches for the current version of the `maven-filtering` dependency in the `pom.xml` file, then updates it to the latest version.

Final Answer:
Updated the `maven-filtering` dependency to the latest version.
        """

        agent = MavenDependencyAgent(None, Path(os.getcwd()), 1)
        result = agent.parse_llm_response(content)
        expected = _llm_response(
            actions=[
                _action(
                    code="""result = search_fqdn.run(artifact_id="maven-filtering", group_id="org.apache.maven.shared")
start_line, end_line = find_in_pom._run(relative_file_path="pom.xml", keywords={"groupId": "org.apache.maven.shared", "artifactId": "maven-filtering"})
xml = f"<dependency><groupId>{result.groupId}</groupId><artifactId>{result.artifactId}</artifactId><version>{result.version}</version></dependency>"
result = editor._run(relative_file_path="pom.xml", start_line=start_line, end_line=end_line, patch=xml)""",
                    thought="The error message indicates that the dependency `org.apache.maven.shared:maven-filtering` is missing. I need to find the current version of this dependency in the `pom.xml` file and update it to the latest version.",
                    observation="The action searches for the current version of the `maven-filtering` dependency in the `pom.xml` file, then updates it to the latest version.",
                ),
            ],
            final_answer="Updated the `maven-filtering` dependency to the latest version.",
        )
        self.assertEqual(expected, result)

    def test_parse_llm_response_multiple_thought(self):
        content = """
Thought: I need to find the current version of the SpringBoot Cache module artifact in the `pom.xml` file.
Action:
```python
start_line, end_line = find_in_pom._run(relative_file_path="pom.xml", keywords={"groupId": "org.springframework.boot", "artifactId": "spring-boot-starter-cache"})
```
Observation: I now have the start and end line of the SpringBoot Cache module artifact in the `pom.xml` file.

Thought: I need to search for the `io.quarkus:quarkus-spring-cache` dependency.
Action:
```python
result = search_fqdn.run(artificat_id="quarkus-spring-cache", group_id="io.quarkus")
```
Observation: I now have the fully qualified domain name for the `io.quarkus:quarkus-spring-cache` dependency.

Thought: I need to replace the SpringBoot Cache module artifact with the `io.quarkus:quarkus-spring-cache` dependency in the `pom.xml` file.
Action:
```python
xml = f"<dependency><groupId>{result.groupId}</groupId><artifactId>{result.artifactId}</artifactId><version>{result.version}</version></dependency>"
result = editor._run(relative_file_path="pom.xml", start_line=start_line, end_line=end_line, patch=xml)
```
Observation: I have replaced the SpringBoot Cache module artifact with the `io.quarkus:quarkus-spring-cache` dependency in the `pom.xml` file.

Final Answer:
Added the `io.quarkus:quarkus-spring-cache` dependency to the `pom.xml` file and replaced the SpringBoot Cache module artifact with it.
```
        """

        agent = MavenDependencyAgent(None, 1)
        expected = _llm_response(
            actions=[
                _action(
                    code='start_line, end_line = find_in_pom._run(relative_file_path="pom.xml", keywords={"groupId": "org.springframework.boot", "artifactId": "spring-boot-starter-cache"})',
                    thought="I need to find the current version of the SpringBoot Cache module artifact in the `pom.xml` file.",
                    observation="I now have the start and end line of the SpringBoot Cache module artifact in the `pom.xml` file.",
                ),
                _action(
                    code='result = search_fqdn.run(artificat_id="quarkus-spring-cache", group_id="io.quarkus")',
                    thought="I need to search for the `io.quarkus:quarkus-spring-cache` dependency.",
                    observation="I now have the fully qualified domain name for the `io.quarkus:quarkus-spring-cache` dependency.",
                ),
                _action(
                    code='xml = f"<dependency><groupId>{result.groupId}</groupId><artifactId>{result.artifactId}</artifactId><version>{result.version}</version></dependency>"\nresult = editor._run(relative_file_path="pom.xml", start_line=start_line, end_line=end_line, patch=xml)',
                    thought="I need to replace the SpringBoot Cache module artifact with the `io.quarkus:quarkus-spring-cache` dependency in the `pom.xml` file.",
                    observation="I have replaced the SpringBoot Cache module artifact with the `io.quarkus:quarkus-spring-cache` dependency in the `pom.xml` file.",
                ),
            ],
            final_answer="Added the `io.quarkus:quarkus-spring-cache` dependency to the `pom.xml` file and replaced the SpringBoot Cache module artifact with it.",
        )
        result = agent.parse_llm_response(content)
        self.assertEqual(expected, result)

    def test_get_query_group_artificat(self):
        @dataclass
        class TestCase:
            code: str
            expected: str

        testCases = [
            TestCase(
                'result = search_fqdn.run(artifact_id="javax.annotation", group_id="javax.annotation")',
                "a:javax.annotation AND g:javax.annotation",
            ),
            TestCase(
                'result = search_fqdn.run(artifact_id="javax.annotation-api")',
                "a:javax.annotation-api",
            ),
            TestCase(
                'result = search_fqdn.run(group_id="javax.annotation")',
                "g:javax.annotation",
            ),
        ]

        MavenDependencyAgent(None, Path(os.getcwd()), 1)

        for t in testCases:
            result = get_maven_query_from_code(t.code)
            self.assertEqual(t.expected, result)

    def test_search_fqdn(self):
        @dataclass
        class TestCase:
            code: str
            expected: FQDNResponse | None

        testCases = [
            TestCase(
                'result = search_fqdn.run(artifact_id="javax.annotation", group_id="javax.annotation")',
                None,
            ),
            TestCase(
                'result = search_fqdn.run(artifact_id="javax.annotation-api", group_id="javax.annotation")',
                FQDNResponse("javax.annotation-api", "javax.annotation", "1.3.2"),
            ),
        ]

        for test in testCases:
            result = search_fqdn(test.code)
            self.assertEqual(test.expected, result)

    def test_find_in_pom(self):
        test_data_dir = Path(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "test_data/test_dependency_agent",
            )
        )

        test_func = find_in_pom(test_data_dir)

        @dataclass
        class TestCase:
            code: str
            expected: FindInPomResponse

        test_cases = [
            TestCase(
                'start_line, end_line = open_file_gen._run(relative_file_path="module/file.py", keywords={"groupId": "org.jboss.spec.javax.jms", "artifactId": "jboss-jms-api_2.0_spec"})',
                FindInPomResponse(18, 22),
            ),
            TestCase(
                'start_line, end_line = open_file_gen._run(relative_file_path="module/file.py", keywords={"groupId": "google.com", "artifactId": "guava"})',
                FindInPomResponse(17, 17),
            ),
        ]

        for test in test_cases:
            result = test_func(test.code)
            self.assertEqual(test.expected, result)
