import unittest
from pathlib import Path

from kai.kai_config import KaiConfigModels
from kai.llm_interfacing.model_provider import ModelProvider
from kai.reactive_codeplanner.agent.analyzer_fix.api import AnalyzerFixRequest
from kai.reactive_codeplanner.agent.api import AgentResult
from kai.reactive_codeplanner.agent.maven_compiler_fix.agent import MavenCompilerAgent
from kai.reactive_codeplanner.agent.maven_compiler_fix.api import (
    MavenCompilerAgentRequest,
    MavenCompilerAgentResult,
)


class TestMavenCompilerAgent(unittest.TestCase):

    def test_parse_llm_response_one_thought(self):
        model_provider = ModelProvider(
            KaiConfigModels(
                provider="FakeListChatModel",
                args={
                    "sleep": None,
                    "responses": [
                        "## Updated Java File\n```java\nimport str\nimport class\n```\n## Reasoning\n1. Frobinate the widget\n\n## Additional Information (optional)\ntesting added info",
                    ],
                },
            )
        )

        agent = MavenCompilerAgent(model_provider=model_provider)
        result = agent.execute(
            MavenCompilerAgentRequest(
                file_path=Path(""), file_contents="", line_number=0, message=""
            )
        )
        print(result)
        expected = MavenCompilerAgentResult(
            file_to_modify=Path(""),
            reasoning="\n1. Frobinate the widget\n",
            updated_file_contents="\nimport str\nimport class",
            additional_information="\ntesting added info",
            original_file="",
            message="",
        )
        print(expected)
        self.assertEqual(expected, result)

    def test_invalid_request_type(self):
        model_provider = ModelProvider(
            KaiConfigModels(
                provider="FakeListChatModel",
                args={
                    "sleep": None,
                    "responses": [
                        "These are the steps:\n1. Frobinate the widget\n2. Profit\n",
                    ],
                },
            )
        )

        agent = MavenCompilerAgent(model_provider=model_provider)
        result = agent.execute(
            AnalyzerFixRequest(file_path=Path(""), file_content="", incidents=[])
        )
        print(result)
        expected = AgentResult()
        print(expected)
        self.assertEqual(expected, result)
