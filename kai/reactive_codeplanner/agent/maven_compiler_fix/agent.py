import re

from jinja2 import Template
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from kai.llm_interfacing.model_provider import ModelProvider
from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.api import Agent, AgentRequest, AgentResult
from kai.reactive_codeplanner.agent.maven_compiler_fix.api import (
    MavenCompilerAgentRequest,
    MavenCompilerAgentResult,
)
from kai.rpc_server.chat import get_chatter_contextvar

logger = get_logger(__name__)
chatter = get_chatter_contextvar()


class MavenCompilerAgent(Agent):
    system_message_template = Template(
        """{{ background }}
    I will give you compiler errors and the offending line of code, and you will need to use the file to determine how to fix them. You should only use compiler errors to determine what to fix.

    You must reason through the required changes and rewrite the Java file to make it compile. 

    You will then provide an step-by-step explanation of the changes required so that someone could recreate it in a similar situation.
    """
    )

    chat_message_template = Template(
        """
    [INST]
    ## Compile Errors
    {{compile_errors}}

    ## Input File
    {{src_file_contents}}


    # Output Instructions
    Structure your output in Markdown format such as:

    ## Updated Java File
    Rewrite the java file here

    ## Reasoning 
    Write the step by step reasoning in this markdown section. If you are unsure of a step or reasoning, clearly state you are unsure and why. 

    ## Additional Information (optional)
    If you have additional details or steps that need to be performed, put it here. Say I have completed the changes when you are done explaining the reasoning[/INST]
    """
    )

    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider

    def execute(self, ask: AgentRequest) -> AgentResult:
        chatter.get().chat_simple("MavenCompilerAgent executing...")

        if not isinstance(ask, MavenCompilerAgentRequest):
            return AgentResult()

        try:
            line_of_code = ask.file_contents.split("\n")[ask.line_number]
        except Exception:
            logger.exception(
                "unable to  split file contents and get line from linenumber"
            )
            return MavenCompilerAgentResult()

        system_message = SystemMessage(
            content=self.system_message_template.render(background=ask.background)
        )

        compile_errors = f"Line of code: {line_of_code};\n{ask.message}"
        content = self.chat_message_template.render(
            src_file_contents=ask.file_contents, compile_errors=compile_errors
        )

        chatter.get().chat_simple("Waiting for response from LLM...")

        ai_message = self.model_provider.invoke(
            [system_message, HumanMessage(content=content)],
            ask.cache_path_resolver,
        )

        resp = self.parse_llm_response(ai_message)
        resp.task = ask.task
        resp.file_to_modify = ask.file_path
        resp.message = ask.message
        resp.original_file = ask.file_contents

        msg = "Received response from LLM\n"
        msg += f"File to modify: {ask.file_path}\n"
        msg += f"<details><summary>Reasoning</summary>\n{resp.reasoning}\n</details>\n"
        msg += f"<details><summary>Additional Information</summary>\n{resp.additional_information}\n</details>\n"
        chatter.get().chat_markdown(msg)

        return resp

    def parse_llm_response(self, message: BaseMessage) -> MavenCompilerAgentResult:
        """Private method that will be used to parse the contents and get the results"""

        if isinstance(message.content, list):
            return MavenCompilerAgentResult()

        lines_of_output = message.content.splitlines()

        in_java_file = False
        in_reasoning = False
        in_additional_details = False
        java_file = ""
        reasoning = ""
        additional_details = ""
        for line in lines_of_output:
            # trunk-ignore(cspell/error)
            if re.match(r"(?:##|\*\*)\s+[Uu]pdated.*[Ff]ile", line.strip()):
                in_java_file = True
                in_reasoning = False
                in_additional_details = False
                continue
            # trunk-ignore(cspell/error)
            if re.match(r"(?:##|\*\*)\s+[Rr]easoning", line.strip()):
                in_java_file = False
                in_reasoning = True
                in_additional_details = False
                continue
            # trunk-ignore(cspell/error)
            if re.match(r"(?:##|\*\*)\s+[Aa]dditional\s+[Ii]nformation", line.strip()):
                in_reasoning = False
                in_java_file = False
                in_additional_details = True
                continue
            if in_java_file:
                if re.match(r"```(?:\w*)", line):
                    continue
                java_file = "\n".join([java_file, line]).strip()
            if in_reasoning:
                reasoning = "\n".join([reasoning, line])
            if in_additional_details:
                additional_details = "\n".join([additional_details, line])
        return MavenCompilerAgentResult(
            reasoning=reasoning,
            updated_file_contents=java_file,
            additional_information=additional_details,
        )
