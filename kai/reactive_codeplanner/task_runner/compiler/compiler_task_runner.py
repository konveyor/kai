from dataclasses import dataclass, field
from pathlib import Path

from jinja2 import Template
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.reflection_agent import ReflectionTask
from kai.reactive_codeplanner.task_manager.api import Task, TaskResult
from kai.reactive_codeplanner.task_runner.api import TaskRunner
from kai.reactive_codeplanner.task_runner.compiler.maven_validator import (
    AccessControlError,
    AnnotationError,
    MavenCompilerError,
    OtherError,
    SyntaxError,
    TypeMismatchError,
)
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager, SpawningResult

logger = get_logger(__name__)


@dataclass
class MavenCompilerLLMResponse(SpawningResult):
    reasoning: str
    java_file: str
    additional_information: str
    file_path: str = ""
    input_file: str = ""
    input_errors: list[str] = field(default_factory=list)

    def to_reflection_task(self) -> ReflectionTask:
        return ReflectionTask(
            file_path=self.file_path,
            issues=set(self.input_errors),
            reasoning=self.reasoning,
            updated_file=self.java_file,
            original_file=self.input_file,
        )


class MavenCompilerTaskRunner(TaskRunner):
    """This agent is responsible for taking a set of maven compiler issues and solving.

    For a given file it will asking LLM's for the changes that are needed for the at whole file
    returning the results.
    """

    handled_type = (
        SyntaxError,
        TypeMismatchError,
        AnnotationError,
        AccessControlError,
        OtherError,
    )

    system_message = SystemMessage(
        content="""
    I will give you compiler errors and the offending line of code, and you will need to use the file to determine how to fix them. You should only use compiler errors to determine what to fix.

    Make sure that the references to any changed types are kept.

    You must reason through the required changes and rewrite the Java file to make it compile. 

    You will then provide an step-by-step explanation of the changes required tso that someone could recreate it in a similar situation.
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

    def __init__(self, llm: BaseChatModel) -> None:
        self.__llm = llm

    def refine_task(self, errors: list[str]) -> None:
        """We currently do not refine the tasks"""
        return None

    def can_handle_error(self, errors: list[str]) -> bool:
        """We currently do not know if we can handle errors"""
        return False

    def can_handle_task(self, task: Task) -> bool:
        """Will determine if the task if a MavenCompilerError, and if we can handle these issues."""
        return isinstance(task, self.handled_type)

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

        ai_message = self.__llm.invoke(
            [self.system_message, HumanMessage(content=content)]
        )

        resp = self.parse_llm_response(ai_message)
        resp.file_path = task.file
        resp.input_file = src_file_contents
        resp.input_errors = [task.message]

        # rewrite the file, based on the java file returned
        with open(task.file, "w") as f:
            f.write(resp.java_file)

        rcm.commit(f"MavenCompilerTaskRunner changed file {str(task.file)}", resp)

        return TaskResult(modified_files=[Path(task.file)], encountered_errors=[])

    def parse_llm_response(self, message: BaseMessage) -> MavenCompilerLLMResponse:
        """Private method that will be used to parse the contents and get the results"""

        if isinstance(message.content, list):
            return MavenCompilerLLMResponse(
                reasoning="", java_file="", additional_information=""
            )

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
            if line.strip() == "## Additional Information (optional)":
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
            additional_information=additional_details,
        )
