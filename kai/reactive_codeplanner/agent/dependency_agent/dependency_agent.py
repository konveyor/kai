# trunk-ignore-begin(ruff/E402)
# This is needed because we are overriding the parser to get line numbers
# The only way to do that, is tell it not to use the c-version of the parser
# so that we can hook into the parser and add attributes to the element.
import sys

sys.modules["_elementtree"] = None  # type: ignore[assignment]

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional, TypedDict, Union

from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage

from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.api import Agent, AgentRequest, AgentResult
from kai.reactive_codeplanner.agent.dependency_agent.api import (
    FindInPomResponse,
    FQDNResponse,
)
from kai.reactive_codeplanner.agent.dependency_agent.dependency_fqdn_selection import (
    FQDNDependencySelectorAgent,
    FQDNDependencySelectorRequest,
)
from kai.reactive_codeplanner.agent.dependency_agent.util import (
    find_in_pom,
    search_fqdn,
)

# trunk-ignore-end(ruff/E402)

logger = get_logger(__name__)


@dataclass
class MavenDependencyRequest(AgentRequest):

    # message from the analyzer or from the compiler
    message: str = ""


@dataclass
class _action:
    code: str
    thought: str
    observation: str


@dataclass
class MavenDependencyResult(AgentResult):
    final_answer: Optional[str]
    fqdn_response: Optional[FQDNResponse]
    find_in_pom: Optional[FindInPomResponse]


@dataclass
class _llm_response:
    actions: list[_action]
    final_answer: str


class MavenDependencyAgent(Agent):

    sys_msg = SystemMessage(
        """
You are an excellent java developer focused on updating dependencies in a maven `pom.xml` file. 

### Guidelines:
1  Only use the provided and predefined functions as the functions. Do not use any other functions.
2 always search for the fqdn for the dependency to be added or updated
3 Only do a single action at a time
4 Do not try to solve in one action, if the final solution is not do able in a single action, then only output the single action do not add Final Answer in this case,6 If you have to edit the xml, ensure the xml is correct with syntax, dependency, consistent with the file and the codebase.
7 Pay attention to original indentation! Something like this "patch": "    def something(self, s):\n    # Check if something is something\n        return something if the original code is indented with 4 spaces or  "def something(self, s):\n    # Check if something is something\n        return something if the original block is not indented.
8 If you are taking an action, then observation can be empty
9 carefully think through the actions needed before responding 

### Functions:
1. **Editing A File with replaced code block**:
   Arguments:
   - relative_file_path: str - The path to the file to edit.
   - start_line: int - The line number where the original target code block starts.
   - end_line: int - The line number where the original target code block ends.
   - xml: str - xml as a string
   Action:
   ```python
   
   result = editor._run(relative_file_path="module/file.py", start_line=12, end_line=24, patch="<xmlTag><xmlSubTag>value</xmlSubTag></xmlTag>")
   print(result)
   ```
2. **Opening a File and Getting Location**:
   Arguments:
   - relative_file_path: str - The path to the file to open.
   Action:
   ```python
   start_line, end_line = find_in_pom._run(relative_file_path="module/file.py", keywords=["some_function"])
   print(result)
   ```
3. **Searching  For Full Dependency Fully Qualified Domain Name**:
   Arguments:
   - artifact_id: str - The alias name of the symbol to find the definition for.
   - group_id: str - The path to the file where the alias is used.
   - version: Optional[str] - The line number where the alias is used.
   Action:
   ```python
   result = search_fqdn.run(artifact_id="commons-collections4", group_id="org.apache.commons", version="4.5.0-M2")
   print(result)
   ```

### Important Notes:
1 We must always use an exact version from the search for Fully Qualified Domain Name of the dependency that we want to update
3. search_fqdn: use this tool to get the fully qualified domain name of a dependency. This includes the artifactId, groupId and the version.

Use this tool to get all references to a symbol in the codebase. This will help you understand how the symbol is used in the codebase. For example, if you want to know where a function is called, you can use this tool.


### Example:
Thought: replace com.google.guava/guava with org.apache.commons/commons-collections4 to the latest version.


Thought:  I have the groupId and the artifactId for the collections4 library, but I don't have the latest version.
Action: ```python
result = search_fqdn.run(artifact_id="commons-collections4", group_id="org.apache.commons")
```
Observation: We now have the fqdn for the commons-collections4 dependency

Though: Now I have the latest version information I need to find the where guava is in the file to replace it.
Action: ```python
start_line, end_line = find_in_pom._run(relative_file_path="module/file.py", keywords={"groupId": "com.google.guava"", "artifactId": "guava")
```
Observation: we now have the start and end line of the in the pom file to be updated

Thought: Now that I have the latest version information and the current start_line and end_line I need to replace the dependency
Action: ```python
xml =  f"<dependency><groupId>{result.groupId}</groupId><artifactId>{result.artifactId}</artifactId><version>{result.version}</version></dependency>"
result = editor._run(relative_file_path="pom.xml", start_line=start_line, end_line=end_line, patch=xml)
print(result)
```
Observation: The pom.xml file is now updated setting the xml at start line with the new dependency to the end line

Final Answer:
Updated the guava to the commons-collections4 dependency
    """
    )

    inst_msg_template = HumanMessagePromptTemplate.from_template(
        """
[INST]
Given the message, you should determine the dependency that needs to be changed.

You must use the following format:

Thought: you should always think about what to do based on the guidelines
Action: the action as block of code to take
Observation: output what the goal of the action is achieving 

When completed, add Final Answer that tells the steps taken


If you are at the point of editing, add the final answer of what you did

Message:{message}
    """
    )

    AgentMethods = TypedDict(
        "AgentMethods",
        {
            "search_fqdn.run": Callable[
                [str], Optional[FQDNResponse] | list[FQDNResponse]
            ],
            "find_in_pom._run": Callable[[str], FindInPomResponse] | None,
        },
    )
    agent_methods: AgentMethods = {
        "search_fqdn.run": search_fqdn,
        "find_in_pom._run": None,
    }

    def __init__(
        self,
        llm: BaseChatModel,
        project_base: Path,
        retries: int = 1,
    ) -> None:
        self.__llm = llm
        self._retries = retries
        self.child_agent = FQDNDependencySelectorAgent(llm=llm)
        self.agent_methods.update({"find_in_pom._run": find_in_pom(project_base)})

    def execute(self, ask: AgentRequest) -> AgentResult:
        if not isinstance(ask, MavenDependencyRequest):
            return AgentResult(encountered_errors=[], modified_files=[])

        request: MavenDependencyRequest = ask

        if not request.message:
            return AgentResult(None, None)

        msg = [self.sys_msg, self.inst_msg_template.format(message=request.message)]
        fix_gen_attempts = 0
        llm_response: Optional[_llm_response] = None
        maven_search: Optional[FQDNResponse] = None
        find_pom_lines: Optional[FindInPomResponse] = None

        # TODO: shawn-hurley: this is needs to be different to allow for the sub-agent's that are needed.
        # We need a sub-agent in the case when searching for the fqdn does not return a single result or
        # no result. In this case we will want the sub agent to try and give us additional information.
        # Today, if we don't have the FQDN then we are going to skip updating for now.

        while fix_gen_attempts < self._retries:
            fix_gen_attempts += 1

            fix_gen_response = self.__llm.invoke(msg)
            llm_response = self.parse_llm_response(fix_gen_response.content)
            # Break out of the while loop, if we don't have a final answer then we need to retry
            if llm_response is None or not llm_response.final_answer:
                break

            # We do not believe that we should not continue now we have to continue after running the code that is asked to be run.
            # The only exception to this rule, is when we actually update the file, that should be handled by the caller.
            # This happens sometimes that the LLM will stop and wait for more information.

            for action in llm_response.actions:
                for method_name, method in self.agent_methods.items():
                    if method_name in action.code:
                        if callable(method):
                            method_out = method(action.code)
                            to_llm_message = getattr(method_out, "to_llm_message", None)
                            if callable(to_llm_message):
                                msg.append(method_out.to_llm_message())

            self._retries += 1

        if llm_response is None or fix_gen_response is None:
            return AgentResult(encountered_errors=[], modified_files=[])

        if not maven_search:
            for a in llm_response.actions:
                if "search_fqdn.run" in a.code:
                    logger.debug("running search for FQDN")
                    _search_fqdn: Callable[
                        [str], Optional[FQDNResponse] | list[FQDNResponse]
                    ] = self.agent_methods["search_fqdn.run"]
                    result = _search_fqdn(a.code)
                    if not result or isinstance(result, list):
                        logger.info("Need to call sub-agent for selecting FQDN")
                        r = self.child_agent.execute(
                            FQDNDependencySelectorRequest(
                                request.file_path,
                                request.message,
                                a.code,
                                query=[],
                                times=0,
                            )
                        )
                        if r.response is not None and isinstance(r.response, list):
                            r.response = None
                        maven_search = r.response
                        if not r.response:
                            logger.debug("unable to get response from sub-agent")
                    else:
                        maven_search = result

        if not find_pom_lines:
            for a in llm_response.actions:
                if "find_in_pom._run" in a.code:
                    logger.debug("running find in pom")
                    _find_in_pom: Optional[Callable[[str], FindInPomResponse]] = (
                        self.agent_methods["find_in_pom._run"]
                    )
                    if _find_in_pom:
                        find_pom_lines = _find_in_pom(a.code)

        # We are going to give back the response, The caller should be responsible for running the code generated by the AI.
        # If we have not take the actions step wise, in the LLM, we need to run all but editor here
        # and give that information to the caller.
        return MavenDependencyResult(
            encountered_errors=None,
            modified_files=None,
            final_answer=llm_response.final_answer,
            fqdn_response=maven_search,
            find_in_pom=find_pom_lines,
        )

    def parse_llm_response(
        # Note, that we have to ignore this type, because it must match LLM
        # Response type and they do not specify the dict args
        self,
        content: Union[str, list[Union[str, dict[Any, Any]]]],
    ) -> Optional[_llm_response]:
        # We should not expect that the value is anything other than str for the type of
        # call that we know we are making
        if isinstance(content, dict) or isinstance(content, list):
            return None

        actions = []
        in_code = False
        in_final_answer = False
        in_thought = False
        in_observation = False
        code_block = ""
        thought_str = ""
        observation_str = ""
        final_answer = ""
        for line in content.splitlines():
            if (
                not line.strip().strip("```")  # trunk-ignore(ruff/B005)
                or line == "```python"
            ):
                continue

            parts = line.split(":")

            if len(parts) > 1:
                match parts[0]:
                    case "Thought":
                        s = ":".join(parts[1:])
                        if code_block or observation_str:
                            actions.append(
                                _action(code_block, thought_str, observation_str)
                            )
                            code_block = ""
                            thought_str = ""
                            observation_str = ""
                            in_observation = False
                        thought_str = s.strip()
                        in_thought = True
                        continue
                    case "Action":
                        in_code = True
                        in_thought = False
                        continue
                    case "Observation":
                        s = ":".join(parts[1:])
                        observation_str = s.strip()
                        in_code = False
                        in_observation = True
                        continue
                    case "Final Answer":
                        actions.append(
                            _action(code_block, thought_str, observation_str)
                        )
                        in_final_answer = True
                        in_code = False
                        in_thought = False
                        continue

            # TODO: There has to be a better way with python to do this.
            if in_code:
                if code_block:
                    code_block = "\n".join([code_block, line.strip()]).strip()
                else:
                    code_block = line.strip()
            if in_final_answer:
                if final_answer:
                    final_answer = "\n".join([final_answer, line]).strip()
                else:
                    final_answer = line.strip()
            if in_thought:
                if thought_str:
                    thought_str = "\n".join([thought_str, line]).strip()
                else:
                    thought_str = line.strip()
            if in_observation:
                if observation_str:
                    observation_str = "\n".join([observation_str, line]).strip()
                else:
                    observation_str = line.strip()
        return _llm_response(actions, final_answer)
