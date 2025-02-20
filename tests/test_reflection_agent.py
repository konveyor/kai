import os
import unittest
from pathlib import Path

from kai.kai_config import KaiConfigModels
from kai.llm_interfacing.model_provider import ModelProvider
from kai.reactive_codeplanner.agent.reflection_agent import (
    ReflectionAgent,
    ReflectionTask,
)
from kai.reactive_codeplanner.task_manager.api import ValidationError


class TestReflectionAgent(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.reflection_agent: ReflectionAgent = ReflectionAgent(
            model_provider=ModelProvider.from_config(
                KaiConfigModels(provider="FakeListChatModel")
            )
        )
        # no need to create another directory for this test as we are mainly
        # testing LLM flow
        self.data_dir_path = Path(
            ".", "tests", "test_data", "test_reflection_agent"
        ).absolute()
        self.original_pom_content = ""
        with open(Path(self.data_dir_path, "pom.xml")) as f:
            self.original_pom_content = f.read()
        # this is a temporary file we use to run tests so we dont clobber checked in files
        self.tc_pom_path = Path(self.data_dir_path, "_pom.xml")
        self.tc_pom_path.touch()

    def tearDown(self) -> None:
        os.remove(self.tc_pom_path)
        return super().tearDown()

    def _set_up_model_provider(self, tc: str) -> None:
        responses = {
            "tc1": [
                "The updated file does not include the full content of the original file. It only includes the updated dependency. However, the updated dependency is correct and replaces the `javaee-api` artifactId with `jakarta.jakartaee-api` as required.\n\n",
                '## Reasoning\n\nWe have updated `javaee-api` with `jakarta.jakartaee-api` and included the full content of the original file.\n\n## Updated file\n\n```xml\n<?xml version="1.0" encoding="UTF-8"?>\n<project \n    xmlns="http://maven.apache.org/POM/4.0.0" \n    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">\n    <modelVersion>4.0.0</modelVersion>\n    <groupId>com.redhat.coolstore</groupId>\n    <artifactId>monolith</artifactId>\n    <version>1.0.0-SNAPSHOT</version>\n    <packaging>war</packaging>\n    <name>coolstore-monolith</name>\n    <properties>\n        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>\n        <maven.build.timestamp.format>yyyyMMdd\'T\'HHmmss</maven.build.timestamp.format>\n        <project.encoding>UTF-8</project.encoding>\n        <maven.test.skip>true</maven.test.skip>\n    </properties>\n    <dependencies>\n        <dependency>\n            <groupId>javax</groupId>\n            <artifactId>javaee-web-api</artifactId>\n            <version>7.0</version>\n            <scope>provided</scope>\n        </dependency>\n        <dependency>\n            <groupId>jakarta.platform</groupId>\n            <artifactId>jakarta.jakartaee-api</artifactId>\n            <version>8.0.0</version>\n            <scope>provided</scope>\n        </dependency>\n        <dependency>\n            <groupId>org.jboss.spec.javax.jms</groupId>\n            <artifactId>jboss-jms-api_2.0_spec</artifactId>\n            <version>2.0.0.Final</version>\n        </dependency>\n        <dependency>\n            <groupId>org.flywaydb</groupId>\n            <artifactId>flyway-core</artifactId>\n            <version>4.1.2</version>\n        </dependency>\n        <dependency>\n            <groupId>org.jboss.spec.javax.rmi</groupId>\n            <artifactId>jboss-rmi-api_1.0_spec</artifactId>\n            <version>1.0.2.Final</version>\n        </dependency>\n    </dependencies>\n    <build>\n        <finalName>ROOT</finalName>\n        <plugins>\n            <plugin>\n                <artifactId>maven-compiler-plugin</artifactId>\n                <version>3.0</version>\n                <configuration>\n                    <encoding>${project.encoding}</encoding>\n                    <source>1.8</source>\n                    <target>1.8</target>\n                </configuration>\n            </plugin>\n            <plugin>\n                <groupId>org.apache.maven.plugins</groupId>\n                <artifactId>maven-war-plugin</artifactId>\n                <version>3.2.0</version>\n            </plugin>\n        </plugins>\n    </build>\n    <profiles>\n<!-- TODO: Add OpenShift profile here -->\n    </profiles>\n</project>\n```',
            ],
            "tc2": [
                "The updated file appears to be valid and addresses the issue identified. The artifact dependency has been updated by replacing the `javaee-api` artifactId with `jakarta.jakartaee-api` as required. The groupId has also been updated to `jakarta.platform` to match the new artifactId. The version has been updated to `8.0.0` which is a valid version for the `jakarta.jakartaee-api` artifact. No unrelated code has been omitted. The file is satisfactory. TERMINATE.",
            ],
        }

        self.reflection_agent = ReflectionAgent(
            model_provider=ModelProvider.from_config(
                config=KaiConfigModels(
                    args={
                        "responses": responses.get(tc, []),
                        "sleep": None,
                    },
                    provider="FakeListChatModel",
                )
            )
        )

    def test_reflection_bad_pom_update(self) -> None:
        self._set_up_model_provider("tc1")

        # this is the update that previous agent made to pom.xml
        updated_pom_content = """<!--Replaced javaee-api dependency-->
<dependency>
    <groupId>jakarta.platform</groupId>
    <artifactId>jakarta.jakartaee-api</artifactId>
    <version>8.0.0</version>
    <scope>provided</scope>
</dependency>
"""
        self.tc_pom_path.write_text(updated_pom_content)

        task = ReflectionTask(
            task=ValidationError(file="test", message="test", line=1, column=1),
            file_path=self.tc_pom_path,
            app_language="Java",
            issues=[
                "Update artifact dependency by replacing the `javaee-api` artifactId with `jakarta.jakartaee-api`",
            ],
            original_file_contents=self.original_pom_content,
            updated_file_contents=updated_pom_content,
            reasoning="We have updated `javaee-api` with `jakarta.jakartaee-api`",
            background="",
        )

        result = self.reflection_agent.execute(task=task)
        self.assertEqual(result.encountered_errors, None)
        self.assertEqual(result.file_to_modify, Path(self.data_dir_path, "_pom.xml"))
        expected_file_contents = Path(
            self.data_dir_path, "expected_pom.xml"
        ).read_text()
        actual_file_contents = Path(self.data_dir_path, "_pom.xml").read_text()
        self.assertEqual(expected_file_contents, actual_file_contents)

    def test_reflection_good_pom_update(self) -> None:
        self._set_up_model_provider("tc2")

        # testing that we terminate as expected when LLM says so
        task = ReflectionTask(
            task=ValidationError(file="test", message="test", line=1, column=1),
            file_path=self.tc_pom_path,
            app_language="Java",
            issues=[
                "Update artifact dependency by replacing the `javaee-api` artifactId with `jakarta.jakartaee-api`",
            ],
            original_file_contents=self.original_pom_content,
            updated_file_contents=Path(
                self.data_dir_path, "expected_pom.xml"
            ).read_text(),
            reasoning="We have updated the dependency to jakarta.jakartaee-api",
            background="",
        )

        result = self.reflection_agent.execute(task=task)

        self.assertEqual(result.encountered_errors, None)
        self.assertEqual(result.file_to_modify, None)
        self.assertEqual(self.tc_pom_path.read_text(), "")
