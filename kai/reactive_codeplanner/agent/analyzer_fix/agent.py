import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, cast

from jinja2 import Template
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from pygments import lexers
from pygments.lexer import LexerMeta
from pygments.util import ClassNotFound

from kai.llm_interfacing.model_provider import ModelProvider
from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.analyzer_fix.api import (
    AnalyzerFixRequest,
    AnalyzerFixResponse,
)
from kai.reactive_codeplanner.agent.api import Agent, AgentRequest

logger = get_logger(__name__)


@dataclass
class _llm_response:
    reasoning: str | None
    java_file: str | None
    addional_information: str | None


class AnalyzerAgent(Agent):
    system_message = SystemMessage(
        content="""
    You are an experienced java developer, who specializes in migrating code to the Quarkus Framework
    """
    )

    chat_message_template = Template(
        """
    I will give you a JavaEE file for which I want to take one step towards migrating to Quarkus.

I will provide you with static source code analysis information highlighting an issue which needs to be addressed.

I will also provide you with an example of how a similar issue was solved in the past via a solved example.

You can refer to the solved example for a pattern of how to update the input Java EE file to Quarkus.

Fix only the problem described. Other problems will be solved in subsequent steps so it is unnecessary to handle them now.

Before attempting to migrate the code to Quarkus reason through what changes are required and why.

Pay attention to changes you make and impacts to external dependencies in the pom.xml as well as changes to imports we need to consider.

Remember when updating or adding annotations that the class must be imported.

As you make changes that impact the pom.xml or imports, be sure you explain what needs to be updated.

After you have shared your step by step thinking, provide a full output of the updated file.

# Input information

## Input File

File name: "{{ src_file_name }}"
Source file contents:
```{{ src_file_language }}
{{ src_file_contents | safe }}
```

## Issues

{% for incident in incidents %}
### incident {{ loop.index0 }}
incident to fix: "{{ incident.message | safe }}"
Line number: {{ incident.line_number }}
{% if incident.solution_str is defined %}
{{ incident.solution_str | safe }}
{% endif %}
{% endfor %}

# Output Instructions
Structure your output in Markdown format such as:

## Reasoning
Write the step by step reasoning in this markdown section. If you are unsure of a step or reasoning, clearly state you are unsure and why.

## Updated File
```java
// Write the updated file for Quarkus in this section. If the file should be removed, make the content of the updated file a comment explaining it should be removed.
```

## Additional Information (optional)

If you have any additional details or steps that need to be performed, put it here.

    """
    )

    def __init__(
        self,
        model_provider: ModelProvider,
        retries: int = 1,
    ) -> None:
        self._model_provider = model_provider
        self._retries = retries

    def execute(self, ask: AgentRequest) -> AnalyzerFixResponse:

        if not isinstance(ask, AnalyzerFixRequest):
            return AnalyzerFixResponse(
                encountered_errors=["invalid request type"],
                file_to_modify=None,
                reasoning=None,
                additional_information=None,
                updated_file_content=None,
            )

        file_name = os.path.basename(ask.file_path)

        language = guess_language(ask.file_content, file_name)

        content = self.chat_message_template.render(
            src_file_contents=ask.file_content,
            src_file_name=file_name,
            src_file_language=language,
            incidents=ask.incidents,
        )

        aimessage = self._model_provider.invoke(
            [self.system_message, HumanMessage(content=content)]
        )

        resp = self.parse_llm_response(aimessage)
        return AnalyzerFixResponse(
            encountered_errors=[],
            file_to_modify=Path(os.path.abspath(ask.file_path)),
            reasoning=resp.reasoning,
            additional_information=resp.addional_information,
            updated_file_content=resp.java_file,
        )

    def parse_llm_response(self, message: BaseMessage) -> _llm_response:
        """Private method that will be used to parse the contents and get the results"""

        lines_of_output = cast(str, message.content).splitlines()

        in_java_file = False
        in_reasoning = False
        in_additional_details = False
        java_file = ""
        reasoning = ""
        additional_details = ""
        for line in lines_of_output:
            if line.strip() == "## Reasoning":
                in_reasoning = True
                in_java_file = False
                in_additional_details = False
                continue
            if line.strip() == "## Updated File":
                in_java_file = True
                in_reasoning = False
                in_additional_details = False
                continue
            if "## Additional Information" in line.strip():
                in_reasoning = False
                in_java_file = False
                in_additional_details = True
                continue
            if in_java_file:
                if "```java" in line or "```" in line:
                    continue
                java_file = "\n".join([java_file, line])
            if in_reasoning:
                reasoning = "\n".join([reasoning, line])
            if in_additional_details:
                additional_details = "\n".join([additional_details, line])
        return _llm_response(
            reasoning=reasoning,
            java_file=java_file,
            addional_information=additional_details,
        )


def guess_language(code: str, filename: Optional[str] = None) -> str:
    try:
        if filename is not None:
            lexer = lexers.guess_lexer_for_filename(filename, code)
            logger.debug(f"{filename} classified as {lexer.aliases[0]}")
        else:
            lexer = cast(LexerMeta, lexers.guess_lexer(code))
            logger.debug(f"Code content classified as {lexer.aliases[0]}\n{code}")
        return lexer.aliases[0]
    except ClassNotFound:
        logger.debug(
            f"Code content for filename {filename} could not be classified\n{code}"
        )
        return "unknown"
