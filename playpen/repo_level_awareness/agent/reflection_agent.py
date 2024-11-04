import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Set

import tree_sitter as ts
import tree_sitter_java as tsj
from langchain.prompts.chat import (
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from playpen.repo_level_awareness.agent.ast_diff.parser import (
    Language,
    extract_ast_info,
)
from playpen.repo_level_awareness.api import Agent, Task, TaskResult
from playpen.repo_level_awareness.task_runner.compiler.compiler_task_runner import (
    MavenCompilerLLMResponse,
)


@dataclass
class ReflectionTask(Task):
    """TODO (pgaikwad): We shouldn't need this class. this is a stop-gap solution as Task is mostly unknown atm"""

    # path to the input file
    file_path: str = ""
    # contents of input file prior to invoking previous agent
    original_file: str = ""
    # contents of updated file produced by previous agent
    updated_file: str = ""
    # reasoning produced by previous agent
    reasoning: str = ""
    # a list of issues originally identified in the file
    issues: Set[str] = ""
    # a keyword describing target technology to act as a hint to agent
    target_technology: str = "Quarkus"


class ReflectionAgent(Agent):
    """Reflection agent reflects on LLM responses of different agents"""

    msg_sys_reflect = SystemMessage(
        content="""You are a senior engineer with extensive experience in developing enterprise Java applications. 
You are helping migrate old Java applications to a newer technology.
A junior engineer has updated a Java file in an application to migrate it to a newer technology.
Use your best judgement to analyze the input data and review the changes.
"""
    )

    msg_templ_sys_fix = SystemMessagePromptTemplate.from_template(
        """You are a senior engineer well versed in Java.
You have extensive experience in migrating enterprise Java applications to newer Java technologies.
You are overseeing a migration of an enterprise Java application to {target_technology}.
You will be given an input file, and a list of migration issues identified in the file.
Fix all the issues described and generate an updated file.
"""
    )

    msg_templ_user_reflect = HumanMessagePromptTemplate.from_template(
        """You will be given a list of migration issues found in an old Java file in JSON format.
Instead of the Java files themselves, you will be given a difference between old file and the new file in JSON format.
The difference is constructed by comparing ASTs of the two files. The JSON keys are self-explanatory.

You will analyze the differences expressed in JSON format to create a mental picture of the old source code and the new.
You will compare the analyzed data with the list of issues and identify which of the issues are not fixed.
Issues often describe the expected change that needs to happen. You will use your best judgement to identify whether the issue is fixed as described.
You will also look for any new changes that were not originally mentioned in the issues.
You will also spot any changes that suggest a change in the original functionality.
If you find an issue that's not fixed, briefly describe why you think the issue is not fixed in 1-2 lines.
If you find unnecessary changes, point those out too.
Be precise in pointing out issues that are not fixed.

## Issues identified in the input file

{issues}

## Differences in ASTs of both files

{diff}
"""
    )

    msg_templ_user_fix = HumanMessagePromptTemplate.from_template(
        """Before attempting to migrate the code to Quarkus reason through what changes are required and why.
Pay attention to changes you make and impacts to external dependencies in the pom.xml as well as changes to imports we need to consider.
Remember when updating or adding annotations that the class must be imported.
As you make changes that impact the pom.xml or imports, be sure you explain what needs to be updated.
After you have shared your step by step thinking, provide a full output of the updated file.
If you are given a feedback, address all the concerns raised in feedback and respond with an updated file.
Structure your output in Markdown format such as:

## Reasoning
Write the step by step reasoning in this markdown section. If you are unsure of a step or reasoning, clearly state you are unsure and why.

## Updated File
```{language}
// Write the updated file for Quarkus in this section. If the file should be removed, make the content of the updated file a comment explaining it should be removed.
```
Here's the input information:

## Input file

```{language}
{input_file}
```

## Issues

{issues}
"""
    )

    msg_templ_ai_fix = AIMessagePromptTemplate.from_template(
        """## Reasoning

{reasoning}

## Updated file

```{language}
{updated_file}
```
"""
    )

    def __init__(
        self,
        llm: BaseChatModel,
        iterations: int = 1,
        retries: int = 1,
        silent: bool = True,
    ) -> None:
        self.__llm = llm
        self._iterations = iterations
        self._retries = retries
        self._silent = silent

    def refine_task(self, errors: list[str]) -> None:
        return super().refine_task(errors)

    def can_handle_error(self, errors: list[str]) -> bool:
        # cannot handle an error right now
        return False

    def can_handle_task(self, task: Task) -> bool:
        if (
            isinstance(task, ReflectionTask)
            and task.issues
            and task.original_file
            and task.updated_file
            and task.reasoning
        ):
            return True
        return False

    def execute_task(self, task: Task) -> TaskResult:
        if not isinstance(task, ReflectionTask):
            return TaskResult(encountered_errors=[], modified_files=[])

        t: ReflectionTask = task

        _, file_ext = os.path.splitext(t.file_path)

        language = {
            ".java": Language.Java,
        }.get(file_ext.lower(), None)

        issues = json.dumps({"issues": list(t.issues)}, indent=4)

        diff = self._get_diff(t.original_file, t.updated_file, language)

        if language is None or not diff or not t.issues:
            return TaskResult(encountered_errors=[], modified_files=[])

        # initiate chats
        chat_fix_gen = [
            self.msg_templ_sys_fix.format(target_technology=t.target_technology),
            self.msg_templ_user_fix.format(
                language=language, input_file=t.original_file, issues=issues
            ),
            self.msg_templ_ai_fix.format(
                language=language, updated_file=t.updated_file, reasoning=t.reasoning
            ),
        ]
        chat_reflect = [
            self.msg_sys_reflect,
            self.msg_templ_user_reflect.format(
                issues=issues,
                diff=json.dumps(diff, indent=4),
            ),
        ]

        modified_files = []
        # run agent loop
        curr_iter = 0
        last_updated_file_contents = t.updated_file
        while curr_iter < self._iterations:
            curr_iter += 1
            try:
                self._out(to="reflection", frm="user", msg=chat_reflect[-1].content)
                reflection_response = self.__llm.invoke(chat_reflect)
                self._out(
                    to="fix-gen", frm="reflection", msg=reflection_response.content
                )
                chat_reflect.append(AIMessage(content=reflection_response.content))
                chat_fix_gen.append(HumanMessage(content=reflection_response.content))
                fix_gen_attempts = 0
                updated_file_contents = None
                fix_gen_response = None
                while fix_gen_attempts < self._retries:
                    fix_gen_attempts += 1
                    fix_gen_response = self.__llm.invoke(chat_fix_gen)
                    self._out(
                        to="reflection", frm="fix-gen", msg=fix_gen_response.content
                    )
                    updated_file_contents = self._parse_llm_response(
                        fix_gen_response.content
                    )
                    if updated_file_contents:
                        break
                if updated_file_contents is None or fix_gen_response is None:
                    return TaskResult(encountered_errors=[], modified_files=[])
                chat_fix_gen.append(AIMessage(content=fix_gen_response.content))
                diff = self._get_diff(last_updated_file_contents, updated_file_contents)
                if not diff:
                    return TaskResult(encountered_errors=[], modified_files=[])
                last_updated_file_contents = updated_file_contents
                chat_reflect.append(
                    self.msg_templ_user_reflect.format(
                        issues=issues, diff=json.dumps(diff)
                    )
                )
            except Exception as e:
                self._out(to="user", frm="agent", msg=f"error occurred: {str(e)}")
                return TaskResult(encountered_errors=[], modified_files=[])

        # commit the result here
        if last_updated_file_contents:
            modified_files.append(t.file_path)
            with open(t.file_path, "w+") as f:
                f.write(last_updated_file_contents)

        return TaskResult(encountered_errors=[], modified_files=modified_files)

    def _get_diff(
        self, original_content: str, updated_content: str, language=Language
    ) -> Dict[str, Any]:
        parser = ts.Parser(ts.Language(tsj.language()))
        original_file_summary = extract_ast_info(
            parser.parse(original_content.encode("utf-8")), language=language
        )
        updated_file_summary = extract_ast_info(
            parser.parse(updated_content.encode("utf-8")), language=language
        )
        if not original_file_summary or not updated_file_summary:
            # this is a case where we will fallback to some
            # other metric for reflection, but right now all
            # other prompts we have used are not reliable. so
            # this is a NOOP right now
            return {}
        diff = original_file_summary.diff(updated_file_summary)
        if not diff:
            # if no diff, we will summarize the updated file instead
            diff = updated_file_summary.to_dict()
        return diff

    def _parse_llm_response(self, content=str) -> str:
        match_updated_file = re.search(
            r"[##|\*\*] [U|u]pdated [F|f]ile\s+.*?```\w+\n([\s\S]*?)```",
            content,
            re.DOTALL,
        )
        if not match_updated_file:
            return None
        return match_updated_file.group(1).strip()

    def _out(self, to: str, frm: str, msg: str):
        if not self._silent:
            print(f"{'*'*10}({frm} -> {to})\n\n{msg}\n")


def reflection_task_from_agent_output(output: Any) -> ReflectionTask:
    match output:
        case MavenCompilerLLMResponse():
            return ReflectionTask(
                file_path=output.file_path,
                issues=set(output.input_errors),
                original_file=output.input_file,
                reasoning=output.reasoning,
                updated_file=output.java_file,
            )
