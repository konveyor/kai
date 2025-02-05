import unittest
from pathlib import Path

from kai.constants import PATH_KAI
from kai.kai_config import KaiConfigModels
from langchain_core.messages import AIMessage
from kai.llm_interfacing.model_provider import ModelProvider
from kai.reactive_codeplanner.agent.analyzer_fix.agent import AnalyzerAgent, _llm_response
from kai.reactive_codeplanner.agent.analyzer_fix.api import (
    AnalyzerFixRequest,
    AnalyzerFixResponse,
)
from kai.reactive_codeplanner.agent.dependency_agent.dependency_agent import (
    MavenDependencyRequest,
)
from kai.reactive_codeplanner.task_manager.api import ValidationError


class TestAnalyzerAgent(unittest.TestCase):

    def test_parse_llm_response_one_thought(self) -> None:
        model_provider = ModelProvider(
            KaiConfigModels(
                provider="FakeListChatModel",
                args={
                    "sleep": None,
                    "responses": [
                        "## Reasoning\n1. Frobinate the widget\n\n## Updated unknown File\n```unknown\nimport str\nimport class\n```\n## Additional Information\ntesting added info",
                    ],
                },
            )
        )

        task = ValidationError(message="test", file="test.yaml", line=1, column=4)
        agent = AnalyzerAgent(model_provider=model_provider)
        result = agent.execute(
            AnalyzerFixRequest(
                file_path=Path(PATH_KAI),
                file_content="",
                incidents=[],
                sources=[],
                targets=[],
                task=task,
                background="",
            )
        )
        print(result)
        expected = AnalyzerFixResponse(
            encountered_errors=[],
            file_to_modify=Path(PATH_KAI),
            reasoning="\n1. Frobinate the widget\n",
            updated_file_content="\nimport str\nimport class",
            additional_information="\ntesting added info",
        )
        print(expected)
        self.assertEqual(expected, result)

    def test_invalid_request_type(self) -> None:
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
        result = agent.execute(
            MavenDependencyRequest(
                Path(""),
                task=ValidationError(message="test", file="test", column=1, line=10),
                background="",
            )
        )
        expected = AnalyzerFixResponse(
            encountered_errors=["invalid request type"],
            file_to_modify=None,
            reasoning=None,
            updated_file_content=None,
            additional_information=None,
        )
        self.assertEqual(expected, result)

    def test_parse_llm_message(self) -> None:
        tc1 = """## Reasoning

1. **blah-blah**: blah blah

## Updated Java File
```java
package a.b.c;

import x.y.z;

@SessionScoped
public class ShoppingCartService  {
}
```

## Additional Information

- **blah-blah**: blah blah

  ```xml
  <dependency>
      <groupId>blah-blah</groupId>
      <artifactId>blah-blah</artifactId>
  </dependency>
  ```
"""
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

        result = agent.parse_llm_response(message=AIMessage(content=tc1))
        expected_result = _llm_response(
            additional_information="""

- **blah-blah**: blah blah

  ```xml
  <dependency>
      <groupId>blah-blah</groupId>
      <artifactId>blah-blah</artifactId>
  </dependency>
  ```""",
            reasoning="""

1. **blah-blah**: blah blah
""",
            source_file="""
package a.b.c;

import x.y.z;

@SessionScoped
public class ShoppingCartService  {
}
""",
        )
        self.assertEqual(result, expected_result)

        tc2 = """** Reasoning

1. **blah-blah**: blah blah

** Updated Java File
```java
package a.b.c;

import x.y.z;

@SessionScoped
public class ShoppingCartService  {
}
```

** Additional Information

- **blah-blah**: blah blah

  ```xml
  <dependency>
      <groupId>blah-blah</groupId>
      <artifactId>blah-blah</artifactId>
  </dependency>
  ```
"""
        result = agent.parse_llm_response(message=AIMessage(content=tc2))
        self.assertEqual(result, expected_result)