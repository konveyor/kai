import re
from dataclasses import dataclass
from typing import Optional, cast

from jinja2 import Template
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import BaseTool, render_text_description

from kai.cache import CachePathResolver
from kai.llm_interfacing.model_provider import ModelProvider
from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agentic.schemas.analyzer_fix.analyzer_fix import (
    AnalysisAgentState,
)
from kai.rpc_server.chat import get_chatter_contextvar

logger = get_logger(__name__)
chatter = get_chatter_contextvar()


@dataclass
class _llm_response:
    reasoning: str | None
    source_file: str | None
    additional_information: str | None


class AnalysisFixNodes:
    def __init__(
        self,
        model: ModelProvider,
        cache_path_resolver: CachePathResolver,
        tools: Optional[list[BaseTool]] = None,
    ):
        self.model = model
        self.cache_path_resolver = cache_path_resolver
        self.tools = tools

    async def analysis_fix_node(self, state: AnalysisAgentState) -> AnalysisAgentState:
        await chatter.get().chat_simple("Fixing analysis issues in the file...")

        file_name = state.input_file_path.name
        source = ",".join(state.sources)
        target = ",".join(state.targets)

        sys_message = SystemMessage(
            content=f"You are an experienced {state.language} developer, who specializes in migrating code from {source} to {target}"
        )

        human_message_template = Template(
            """I will give you a {{ language }} file for which I want to take one step towards migrating to {{ target }}.
I will provide you with static source code analysis information highlighting issues which need to be addressed.
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

        human_message = human_message_template.render(
            source=source,
            target=target,
            language=state.language,
            src_file_contents=state.input_file_content,
            src_file_name=file_name,
            src_file_language=state.language,
            incidents=state.incidents,
        )

        await chatter.get().chat_simple("Waiting for response from LLM...")

        try:
            response = await self.model.ainvoke(
                [sys_message, HumanMessage(content=human_message)],
                self.cache_path_resolver,
            )
        except Exception:
            await chatter.get().chat_simple(
                "Analyzer agent failed to get a fix from LLM..."
            )

        parsed_response = self._parse_llm_response(response)
        msg = "Received response from LLM\n"
        msg += f"File to modify: {state.input_file_path}\n"
        msg += f"<details><summary>Reasoning</summary>\n{parsed_response.reasoning}\n</details>\n"
        msg += f"<details><summary>Additional Information</summary>\n{parsed_response.additional_information}\n</details>\n"
        await chatter.get().chat_markdown(msg)

        state.additional_information = parsed_response.additional_information
        state.reasoning = parsed_response.reasoning
        state.updated_input_file = parsed_response.source_file
        return state

    async def analysis_plan_node(self, state: AnalysisAgentState) -> AnalysisAgentState:
        return state

    async def additional_information_node(
        self, state: AnalysisAgentState
    ) -> AnalysisAgentState:
        source = ",".join(state.sources)
        target = ",".join(state.targets)

        sys_message_content = f"You are an experienced {state.language} developer, who specializes in migrating code\
from {source} to {target}."

        human_message = HumanMessage(
            content=f"""A senior engineer made changes to a file to migrate it. There may be more changes needed elsewhere in the project\
to completely migrate the source code. You are given the engineer's notes detailing the changes needed.\
Carefully analyze the changes and understand what files in the project need to be changed.\
You have access to a set of tools to search for files, read files and write to files.\
Work on one file at a time. Respond with DONE when you're done addressing all the changes.\
{state.additional_information}
"""
        )

        if self.model.tools_supported() and self.tools:
            result = await self.model.llm.bind_tools(self.tools).ainvoke(
                [SystemMessage(content=sys_message_content), human_message]
            )
        elif self.tools:
            sys_message_content = f"{sys_message_content}\nYou have access to following tools to perform actions\n{render_text_description(self.tools)}\n\
If you need to call a tool, respond only with a JSON object containing two keys - `tool_name` and `args`.\
`tool_name` is the name of the tool to call and `args` is a nested JSON object containing arguments to pass to the tool.\
Make sure the JSON object is enclosed within ``` to clearly show the code block."
            result = await self.model.ainvoke(
                [SystemMessage(content=sys_message_content), human_message]
            )

        if "DONE" in result.content:
            state.done = True

        return state

    def _parse_llm_response(self, message: BaseMessage) -> _llm_response:
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
