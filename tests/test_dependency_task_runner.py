import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from kai.kai_config import KaiConfigModels
from kai.llm_interfacing.model_provider import ModelProvider
from kai.reactive_codeplanner.agent.dependency_agent.api import FQDNResponse
from kai.reactive_codeplanner.agent.dependency_agent.dependency_agent import (
    MavenDependencyAgent,
    MavenDependencyResult,
)
from kai.reactive_codeplanner.task_runner.compiler.maven_validator import (
    PackageDoesNotExistError,
)
from kai.reactive_codeplanner.task_runner.dependency.task_runner import (
    DependencyTaskRunner,
)
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager


class TestDependencyTaskRunner(unittest.TestCase):

    def setUp(self):
        self.project_base = Path(
            os.path.abspath(
                Path(".", "tests", "test_data", "test_dependency_task_runner")
            )
        )
        return super().setUp()

    def _task_runner(
        self, project_base: Path, response_variant: int = 0
    ) -> DependencyTaskRunner:
        responses = [
            [
                '\n\n\n\n\n\nThought: The error message indicates that the Maven compiler is unable to find the jakarta.persistence package. This package is typically provided by the Jakarta Persistence API (JPA) dependency. I need to find the fully qualified domain name (FQDN) of the JPA dependency to add it to the pom.xml file.\n\nAction: \n```python\nresult = search_fqdn.run(artifact_id="jakarta.persistence-api", group_id="jakarta.persistence")\n```\nObservation: We now have the FQDN for the Jakarta Persistence API dependency.',
                '\n\n\n\n\n\nThought: Now that I have the FQDN for the Jakarta Persistence API dependency, I need to find the location in the pom.xml file where I can add this dependency.\n\nAction: \n```python\nstart_line, end_line = find_in_pom._run(relative_file_path="pom.xml", keywords=["<dependencies>"])\n```\nObservation: We now have the start and end line of the dependencies block in the pom.xml file.\n\nUser: The result for the location is (12, 13) \n\nAssistant: \n\n\n\n\n\nThought: Now that I have the start and end line of the dependencies block in the pom.xml file, I can add the Jakarta Persistence API dependency.\n\nAction: \n```python\nxml = f"<dependency><groupId>{result.group_id}</groupId><artifactId>{result.artifact_id}</artifactId><version>{result.version}</version></dependency>"\nresult = editor._run(relative_file_path="pom.xml", start_line=12, end_line=13, patch=xml)\nprint(result)\n```\nObservation: The pom.xml file is now updated with the Jakarta Persistence API dependency added.\n\nFinal Answer:\nAdded the Jakarta Persistence API dependency to the pom.xml file. Steps taken:\n1. Searched for the FQDN of the Jakarta Persistence API dependency.\n2. Found the location of the dependencies block in the pom.xml file.\n3. Added the Jakarta Persistence API dependency to the pom.xml file.',
            ],
            [
                """Thought: The error message indicates that the `org.eclipse.microprofile.reactive.messaging` package is missing. This suggests that the dependency for MicroProfile Reactive Messaging is not present in the `pom.xml` file. I need to search for the fully qualified domain name (FQDN) for the MicroProfile Reactive Messaging dependency to add it to the `pom.xml`.

Action: 
```python
result = search_fqdn.run(artifact_id="microprofile-reactive-messaging-api", group_id="org.eclipse.microprofile.reactive.messaging")
```

Observation: This action will provide the FQDN for the MicroProfile Reactive Messaging dependency, including the artifactId, groupId, and version, which is necessary to add the correct dependency to the `pom.xml` file.""",
                """Thought: Now that I have the FQDN for the MicroProfile Reactive Messaging dependency, I need to add this dependency to the `pom.xml` file. I will search for the appropriate location in the `pom.xml` file to insert this dependency.

Action:
```python
start_line, end_line = find_in_pom._run(relative_file_path="pom.xml", keywords=["dependencies"])
```

Observation: This action will help me find the location of the `<dependencies>` section in the `pom.xml` file, where I can add the new dependency for MicroProfile Reactive Messaging.""",
                """Thought: With the start and end lines of the `<dependencies>` section identified, I can now proceed to add the MicroProfile Reactive Messaging dependency to the `pom.xml` file.

Action:
```python
xml = "<dependency><groupId>org.eclipse.microprofile.reactive.messaging</groupId><artifactId>microprofile-reactive-messaging-api</artifactId><version>3.0.1</version></dependency>"
result = editor._run(relative_file_path="pom.xml", start_line=2, end_line=2, patch=xml)
print(result)
```

Observation: This action will insert the MicroProfile Reactive Messaging dependency into the `pom.xml` file at the correct location, ensuring that the package is available for use in the project.

Final Answer: Added the MicroProfile Reactive Messaging dependency with groupId `org.eclipse.microprofile.reactive.messaging`, artifactId `microprofile-reactive-messaging-api`, and version `3.0.1` to the `pom.xml` file.""",
            ],
        ]
        return DependencyTaskRunner(
            MavenDependencyAgent(
                model_provider=ModelProvider(
                    config=KaiConfigModels(
                        args={
                            "responses": responses[response_variant],
                            "sleep": None,
                        },
                        provider="FakeListChatModel",
                    )
                ),
                project_base=project_base,
            )
        )

    def test_package_does_not_exist_task(self) -> None:
        task = PackageDoesNotExistError(
            priority=1,
            parse_lines="'[ERROR] ./test_data/test_dependency_agent/Order.java:[8,27] package jakarta.persistence does not exist'",
            missing_package="jakarta.persistence",
            message="package jakarta.persistence does not exist",
            file=str(self.project_base / "Order.java"),
            line=8,
            max_retries=3,
            column=27,
        )

        runner = self._task_runner(project_base=self.project_base, response_variant=0)

        rcm = RepoContextManager(project_root=self.project_base)
        snapshot = rcm.snapshot
        result = runner.execute_task(rcm=rcm, task=task)

        self.assertEqual(len(result.modified_files), 1)

        if result.modified_files:
            modified_pom = result.modified_files[0]
            with open(modified_pom) as f:
                actual_pom_contents = f.read()
            with open(self.project_base / "expected_pom.xml") as f:
                expected_pom_contents = f.read()
            self.assertEqual(actual_pom_contents, expected_pom_contents)

        rcm.reset(snapshot)

    def test_package_does_not_exist_error_bug_616(self) -> None:
        task = PackageDoesNotExistError(
            priority=1,
            parse_lines="'[ERROR] ./test_data/test_dependency_agent/Order.java:[8,27] package jakarta.persistence does not exist'",
            missing_package="jakarta.persistence",
            message="Maven compiler error: package org.eclipse.microprofile.reactive.messaging does not exist",
            file=str(self.project_base / "Order.java"),
            line=8,
            max_retries=3,
            column=27,
        )

        runner = self._task_runner(project_base=self.project_base, response_variant=1)

        rcm = RepoContextManager(project_root=self.project_base)
        snapshot = rcm.snapshot
        result = runner.execute_task(rcm=rcm, task=task)

        self.assertEqual(len(result.modified_files), 1)

        if result.modified_files:
            modified_pom = result.modified_files[0]
            with open(modified_pom) as f:
                actual_pom_contents = f.read()
            with open(self.project_base / "expected_pom_bug_616.xml") as f:
                expected_pom_contents = f.read()
            self.assertEqual(actual_pom_contents, expected_pom_contents)

        rcm.reset(snapshot)

    def test_deduplicate_deps(self) -> None:
        mock_agent = MagicMock()
        mock_agent.execute.return_value = MavenDependencyResult(
            encountered_errors=[],
            file_to_modify=Path("pom.xml"),
            final_answer="Found the answer",
            find_in_pom=None,
            fqdn_response=FQDNResponse(
                artifact_id="smallrye-reactive-messaging",
                group_id="io.smallrye.reactive",
                version="4.29.0",
            ),
        )
        rcm = RepoContextManager(project_root=self.project_base / "deduplication")
        task_runner = DependencyTaskRunner(
            agent=mock_agent,
        )
        pom_file = self.project_base / "deduplication" / "pom.xml"
        result = task_runner.execute_task(
            rcm=rcm,
            task=PackageDoesNotExistError(
                priority=1,
                parse_lines="'[ERROR] ./test_data/test_dependency_agent/Order.java:[8,27] package jakarta.persistence does not exist'",
                missing_package="jakarta.persistence",
                message="Maven compiler error: package org.eclipse.microprofile.reactive.messaging does not exist",
                file=str(self.project_base / "Order.java"),
                line=8,
                max_retries=3,
                column=27,
            ),
        )
        self.assertEqual(result.encountered_errors, [])
        self.assertEqual(result.modified_files, [pom_file])
        expected_file = self.project_base / "deduplication" / "expected.xml"
        self.assertEqual(pom_file.read_text(), expected_file.read_text())
        rcm.reset(rcm.first_snapshot)
