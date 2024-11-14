import unittest
from pathlib import Path

from dotenv import load_dotenv

from kai.kai_config import KaiConfigModels
from kai.llm_interfacing.model_provider import ModelProvider
from kai.reactive_codeplanner.agent.dependency_agent.dependency_agent import (
    MavenDependencyAgent,
)
from kai.reactive_codeplanner.task_runner.compiler.maven_validator import (
    PackageDoesNotExistError,
)
from kai.reactive_codeplanner.task_runner.dependency.task_runner import (
    DependencyTaskRunner,
)
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager


class TestDependencyTaskRunner(unittest.TestCase):

    def _task_runner(
        self, project_base: Path, response_variant: int = 0
    ) -> DependencyTaskRunner:
        responses = [
            [
                '\n\n\n\n\n\nThought: The error message indicates that the Maven compiler is unable to find the jakarta.persistence package. This package is typically provided by the Jakarta Persistence API (JPA) dependency. I need to find the fully qualified domain name (FQDN) of the JPA dependency to add it to the pom.xml file.\n\nAction: \n```python\nresult = search_fqdn.run(artifact_id="jakarta.persistence-api", group_id="jakarta.persistence")\n```\nObservation: We now have the FQDN for the Jakarta Persistence API dependency.',
                '\n\n\n\n\n\nThought: Now that I have the FQDN for the Jakarta Persistence API dependency, I need to find the location in the pom.xml file where I can add this dependency.\n\nAction: \n```python\nstart_line, end_line = find_in_pom._run(relative_file_path="pom.xml", keywords=["<dependencies>"])\n```\nObservation: We now have the start and end line of the dependencies block in the pom.xml file.\n\nUser: The result for the location is (12, 13) \n\nAssistant: \n\n\n\n\n\nThought: Now that I have the start and end line of the dependencies block in the pom.xml file, I can add the Jakarta Persistence API dependency.\n\nAction: \n```python\nxml = f"<dependency><groupId>{result.group_id}</groupId><artifactId>{result.artifact_id}</artifactId><version>{result.version}</version></dependency>"\nresult = editor._run(relative_file_path="pom.xml", start_line=12, end_line=13, patch=xml)\nprint(result)\n```\nObservation: The pom.xml file is now updated with the Jakarta Persistence API dependency added.\n\nFinal Answer:\nAdded the Jakarta Persistence API dependency to the pom.xml file. Steps taken:\n1. Searched for the FQDN of the Jakarta Persistence API dependency.\n2. Found the location of the dependencies block in the pom.xml file.\n3. Added the Jakarta Persistence API dependency to the pom.xml file.',
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
        project_base = Path(
            ".", "tests", "test_data", "test_dependency_task_runner"
        ).absolute()

        task = PackageDoesNotExistError(
            priority=1,
            parse_lines="'[ERROR] ./test_data/test_dependency_agent/Order.java:[8,27] package jakarta.persistence does not exist'",
            missing_package="jakarta.persistence",
            message="package jakarta.persistence does not exist",
            file=str(project_base / "Order.java"),
            line=8,
            max_retries=3,
            column=27,
        )

        runner = self._task_runner(project_base=project_base, response_variant=0)

        rcm = RepoContextManager(project_root=project_base)
        result = runner.execute_task(rcm=rcm, task=task)

        self.assertEqual(len(result.modified_files), 1)

        if result.modified_files:
            modified_pom = result.modified_files[0]
            with open(modified_pom) as f:
                actual_pom_contents = f.read()
            with open(project_base / "expected_pom.xml") as f:
                expected_pom_contents = f.read()
            self.assertEqual(actual_pom_contents, expected_pom_contents)

        rcm.reset_to_first()
