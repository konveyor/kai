from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional, TypedDict, Union

from jinja2 import Template
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from kai.llm_interfacing.model_provider import ModelProvider
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
from kai.rpc_server.chat import get_chatter_contextvar

logger = get_logger(__name__)
chatter = get_chatter_contextvar()


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
    final_answer: Optional[str] = None
    fqdn_response: Optional[FQDNResponse] = None
    find_in_pom: Optional[FindInPomResponse] = None


@dataclass
class _llm_response:
    actions: list[_action]
    final_answer: str


class MavenDependencyAgent(Agent):

    system_message_template = Template(
        """
You are an excellent java developer focused on updating dependencies in a maven `pom.xml` file. 
{{ background }}

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

Thought: Now I have the latest version information I need to find the where guava is in the file to replace it.
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
Given the message, you should determine the dependency that needs to be changed.

You must use the following format:

Thought: you should always think about what to do based on the guidelines
Action: the action as block of code to take
Observation: output what the goal of the action is achieving 

When completed, add Final Answer that tells the steps taken


If you are at the point of editing, add the final answer of what you did

Message:

    {message}
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
        model_provider: ModelProvider,
        project_base: Path,
        retries: int = 3,
    ) -> None:
        self._model_provider = model_provider
        self._max_retries = retries
        self.child_agent = FQDNDependencySelectorAgent(model_provider=model_provider)
        self.agent_methods.update({"find_in_pom._run": find_in_pom(project_base)})

    async def execute(self, ask: AgentRequest) -> AgentResult:
        await chatter.get().chat_simple("MavenDependencyAgent executing...")

        if not isinstance(ask, MavenDependencyRequest):
            return AgentResult()

        request: MavenDependencyRequest = ask

        if not request.message:
            return AgentResult()

        system_message = SystemMessage(
            content=self.system_message_template.render(background=ask.background)
        )

        content = self.inst_msg_template.format(message=request.message)

        msg = [system_message, content]
        fix_gen_attempts = 0
        llm_response: Optional[_llm_response] = None
        maven_search: Optional[FQDNResponse] = None
        find_pom_lines: Optional[FindInPomResponse] = None

        # TODO: shawn-hurley: this is needs to be different to allow for the sub-agent's that are needed.
        # We need a sub-agent in the case when searching for the fqdn does not return a single result or
        # no result. In this case we will want the sub agent to try and give us additional information.
        # Today, if we don't have the FQDN then we are going to skip updating for now.

        all_actions: list[_action] = []
        while fix_gen_attempts < self._max_retries:
            fix_gen_attempts += 1

            fix_gen_response = await self._model_provider.ainvoke(
                msg, cache_path_resolver=ask.cache_path_resolver
            )
            llm_response = self.parse_llm_response(fix_gen_response.content)

            # if we don't have a final answer, we need to retry, otherwise break
            if llm_response is not None and llm_response.final_answer:
                all_actions.extend(llm_response.actions)
                break

            # we have to keep the chat going until we get a final answer
            msg.append(AIMessage(content=fix_gen_response.content))

            if llm_response is None or not llm_response.actions:
                msg.append(
                    HumanMessage(
                        content="Please provide a complete response until at least one action to perform."
                    )
                )
                continue

            all_actions.extend(llm_response.actions)
            tool_outputs: list[str] = []
            for action in llm_response.actions:
                for method_name, method in self.agent_methods.items():
                    if method_name in action.code:
                        if callable(method):
                            method_out = method(action.code)
                            to_llm_message: Optional[Callable[[], HumanMessage]] = (
                                getattr(method_out, "to_llm_message", None)
                            )
                            if to_llm_message is not None and callable(to_llm_message):
                                tool_outputs.append(method_out.to_llm_message().content)
            if tool_outputs:
                msg.append(HumanMessage(content="\n".join(tool_outputs)))
            else:
                # we cannot continue the chat when we dont have any tool outputs
                break

        if llm_response is None or fix_gen_response is None:
            return AgentResult()

        if not maven_search:
            for a in all_actions:
                if "search_fqdn.run" in a.code:
                    logger.debug("running search for FQDN")
                    _search_fqdn: Callable[
                        [str], Optional[FQDNResponse] | list[FQDNResponse]
                    ] = self.agent_methods["search_fqdn.run"]
                    result = _search_fqdn(a.code)
                    if not result or isinstance(result, list):
                        logger.info("Need to call sub-agent for selecting FQDN")
                        r = await self.child_agent.execute(
                            FQDNDependencySelectorRequest(
                                file_path=request.file_path,
                                task=ask.task,
                                msg=request.message,
                                code=a.code,
                                query=[],
                                times=0,
                                background=ask.background,
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
            for a in all_actions:
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
        if (
            not llm_response.final_answer
            and maven_search is not None
            and maven_search.version
        ):
            llm_response.final_answer = "found dependency"
        return MavenDependencyResult(
            encountered_errors=None,
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
                match parts[0].strip():
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
                        if code_block:
                            actions.append(
                                _action(code_block, thought_str, observation_str)
                            )
                            code_block = ""
                            thought_str = ""
                            observation_str = ""
                        final_answer = " ".join(parts[1:]).strip()
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

        if code_block and thought_str and observation_str:
            actions.append(_action(code_block, thought_str, observation_str))

        return _llm_response(actions, final_answer)
