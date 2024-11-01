import unittest
from pathlib import Path

from kai.kai_config import KaiConfigModels
from kai.llm_interfacing.model_provider import ModelProvider
from kai.reactive_codeplanner.agent.analyzer_fix.agent import AnalyzerAgent
from kai.reactive_codeplanner.agent.analyzer_fix.api import (
    AnalyzerFixRequest,
    AnalyzerFixResponse,
)
from kai.reactive_codeplanner.agent.dependency_agent.dependency_agent import (
    MavenDependencyRequest,
)


class TestAnalyzerAgent(unittest.TestCase):

    def test_parse_llm_response_one_thought(self):
        model_provider = ModelProvider(
            KaiConfigModels(
                provider="FakeListChatModel",
                args={
                    "sleep": None,
                    "responses": [
                        "## Reasoning\n1. Frobinate the widget\n\n## Updated Java File\n```java\nimport str\nimport class\n```\n## ## Additional Information\ntesting added info",
                    ],
                },
            )
        )

        agent = AnalyzerAgent(model_provider=model_provider)
        result = agent.execute(
            AnalyzerFixRequest(file_path=Path(""), file_content="", incidents="")
        )
        print(result)
        expected = AnalyzerFixResponse(
            encountered_errors=[],
            file_to_modify=Path(""),
            reasoning="\n1. Frobinate the widget\n",
            updated_file_content="\nimport str\nimport class",
            additional_information="\ntesting added info",
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

        agent = AnalyzerAgent(model_provider=model_provider)
        result = agent.execute(MavenDependencyRequest(Path("")))
        print(result)
        expected = AnalyzerFixResponse(
            encountered_errors=["invalid request type"],
            file_to_modify=Path(""),
            reasoning=None,
            updated_file_content=None,
            additional_information=None,
        )
        print(expected)
        self.assertEqual(expected, result)
