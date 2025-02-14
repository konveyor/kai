import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from jinja2 import Template
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from kai.llm_interfacing.model_provider import ModelProvider
from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.analyzer_fix.api import (
    AnalyzerFixRequest,
    AnalyzerFixResponse,
)
from kai.reactive_codeplanner.agent.analyzer_fix.guess_language import guess_language
from kai.reactive_codeplanner.agent.api import Agent, AgentRequest
from kai.rpc_server.chat import get_chatter_contextvar

logger = get_logger(__name__)
chatter = get_chatter_contextvar()


@dataclass
class _llm_response:
    reasoning: str | None
    source_file: str | None
    additional_information: str | None


class AnalyzerAgent(Agent):
    system_message_template = Template(
        """
    You are an experienced {{ language }} developer, who specializes in migrating code from {{ source }} to {{ target }}
    {{ background }}
    """
    )

    chat_message_template = Template(
        """
    I will give you a {{ source }} file for which I want to take one step towards migrating to {{ target }}.

I will provide you with static source code analysis information highlighting an issue which needs to be addressed.

Fix all the issues described. Other problems will be solved in subsequent steps so it is unnecessary to handle them now.

Before attempting to migrate the code to {{ target }} reason through what changes are required and why.

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

## Updated {{ language }} File
```{{ language }}
// Write the updated file in this section. If the file should be removed, make the content of the updated file a comment explaining it should be removed.
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
        chatter.get().chat_simple("AnalyzerAgent executing...")

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

        source = " and ".join(ask.sources)
        target = " and ".join(ask.targets)

        system_message = SystemMessage(
            content=self.system_message_template.render(
                language=language,
                source=source,
                target=target,
                background=ask.background,
            )
        )

        content = self.chat_message_template.render(
            source=source,
            target=target,
            language=language,
            src_file_contents=ask.file_content,
            src_file_name=file_name,
            src_file_language=language,
            incidents=ask.incidents,
        )

        chatter.get().chat_simple("Waiting for response from LLM...")

        ai_message = self._model_provider.invoke(
            [system_message, HumanMessage(content=content)],
            ask.cache_path_resolver,
        )

        resp = self.parse_llm_response(ai_message)

        msg = "Received response from LLM\n"
        msg += f"File to modify: {ask.file_path}\n"
        msg += f"<details><summary>Reasoning</summary>\n{resp.reasoning}\n</details>\n"
        msg += f"<details><summary>Additional Information</summary>\n{resp.additional_information}\n</details>\n"
        chatter.get().chat_markdown(msg)

        return AnalyzerFixResponse(
            encountered_errors=[],
            file_to_modify=Path(os.path.abspath(ask.file_path)),
            reasoning=resp.reasoning,
            additional_information=resp.additional_information,
            updated_file_content=resp.source_file,
        )

    def parse_llm_response(self, message: BaseMessage) -> _llm_response:
        """Private method that will be used to parse the contents and get the results"""

        lines_of_output = cast(str, message.content).splitlines()

        in_source_file = False
        in_reasoning = False
        in_additional_details = False
        source_file = ""
        reasoning = ""
        additional_details = ""
        for line in lines_of_output:
            # trunk-ignore(cspell/error)
            if re.match(r"(?:##|\*\*)\s+[Rr]easoning", line.strip()):
                in_reasoning = True
                in_source_file = False
                in_additional_details = False
                continue
            # trunk-ignore(cspell/error)
            if re.match(r"(?:##|\*\*)\s+[Uu]pdated.*[Ff]ile", line.strip()):
                in_source_file = True
                in_reasoning = False
                in_additional_details = False
                continue
            # trunk-ignore(cspell/error)
            if re.match(r"(?:##|\*\*)\s+[Aa]dditional\s+[Ii]nformation", line.strip()):
                in_reasoning = False
                in_source_file = False
                in_additional_details = True
                continue
            if in_source_file:
                if re.match(r"```(?:\w*)", line):
                    continue
                source_file = "\n".join([source_file, line])
            if in_reasoning:
                reasoning = "\n".join([reasoning, line])
            if in_additional_details:
                additional_details = "\n".join([additional_details, line])
        return _llm_response(
            reasoning=reasoning,
            source_file=source_file,
            additional_information=additional_details,
        )
