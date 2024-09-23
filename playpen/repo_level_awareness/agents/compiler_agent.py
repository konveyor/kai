from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from jinja2 import Template
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from playpen.repo_level_awareness.api import Agent, Task, TaskResult
from playpen.repo_level_awareness.git_vfs import RepoContextManager
from playpen.repo_level_awareness.maven_validator import MavenCompilerError


@dataclass
class MavenCompilerLLMResponse:
    reasoning: str
    java_file: str
    addional_information: str
    file_path: str = ""
    input_file: str = ""
    input_errors: List[str] = field(factory_method=list)


class MavenCompilerAgent(Agent):
    """This agent is reponsible for taking a set of maven compiler issues and solving.

    For a given file it will asking LLM's for the changes that are needed for the at whole file
    returning the results.
    """

    system_message = SystemMessage(
        content="""
    I will give you compiler errors and the offending line of code, and you will need to use the file to determine how to fix them. You should only use compiler errors to determine what to fix.

    Make sure that the references to any changed types are kept.

    You must reason through the required changes and rewrite the Java file to make it compile. 

    You will then provide an step-by-step explaination of the changes required tso that someone could recreate it in a similar situation. 
    """
    )

    chat_message_template = Template(
        """
    [INST]
    ## Compile Errors
    {{compile_errors}}

    ## Input File
    {{src_file_contents}}


    # Ouput Instructions 
    Structure your output in Markdown format such as:

    ## Updated Java File
    Rewrite the java file here

    ## Reasoning 
    Write the step by step reasoning in this markdown section. If you are unsure of a step or reasoning, clearly state you are unsure and why. 

    ## Additional Infomation (optional)
    If you have additional details or steps that need to be perfomed, put it here. Say I have completed the changes when you are done explaining the reasoning[/INST]
    """
    )

    def __init__(self, llm: BaseChatModel) -> None:
        self.__llm = llm

    def refine_task(self, errors: list[str]) -> None:
        """We currently do not refine the tasks"""
        return super().refine_task(errors)

    def can_handle_error(self, errors: list[str]) -> bool:
        """We currently do not know if we can handle errors"""
        return super().can_handle_error(errors)

    def can_handle_task(self, task: Task) -> bool:
        """Will determine if the task if a MavenCompilerError, and if we can handle these issues."""
        print(task)
        return isinstance(task, MavenCompilerError)

    def execute_task(self, rcm: RepoContextManager, task: Task) -> TaskResult:
        """This will be responsible for getting the full file from LLM and updating the file on disk"""

        # convert the task to the MavenCompilerError
        if not isinstance(task, MavenCompilerError):
            return TaskResult(encountered_errors=[], modified_files=[])

        with open(task.file) as f:
            src_file_contents = f.read()

        line_of_code = src_file_contents.split("\n")[task.line]

        compile_errors = f"Line of code: {line_of_code};\n{task.message}"

        content = self.chat_message_template.render(
            src_file_contents=src_file_contents, compile_errors=compile_errors
        )

        aimessage = self.__llm.invoke(
            [self.system_message, HumanMessage(content=content)]
        )

        resp = self.parse_llm_response(aimessage)
        print(resp)
        resp.file_path = task.file
        resp.input_file = src_file_contents
        resp.input_errors = [task.message]

        # rewrite the file, based on the java file returned
        with open(task.file, "w") as f:
            f.write(resp.java_file)

        rcm.commit("compiler", resp)

        return TaskResult(modified_files=[Path(task.file)], encountered_errors=[])

    def parse_llm_response(self, message: BaseMessage) -> MavenCompilerLLMResponse:
        """Private method that will be used to parse the contents and get the results"""

        print(message.content)

        lines_of_output = message.content.splitlines()

        in_java_file = False
        in_reasoning = False
        in_additional_details = False
        java_file = ""
        reasoning = ""
        additional_details = ""
        for line in lines_of_output:
            if line.strip() == "## Updated Java File":
                in_java_file = True
                continue
            if line.strip() == "## Reasoning":
                in_java_file = False
                in_reasoning = True
                continue
            if line.strip() == "## Additional Infomation (optional)":
                in_reasoning = False
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
        return MavenCompilerLLMResponse(
            reasoning=reasoning,
            java_file=java_file,
            addional_information=additional_details,
        )
