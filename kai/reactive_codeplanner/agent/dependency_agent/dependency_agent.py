from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional, TypedDict, Union

from jinja2 import Template
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

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
    fqdn_response: Optional[FQDNResponse] = None


@dataclass
class _llm_response:
    actions: list[_action]
    final_answer: str


class MavenDependencyAgent(Agent):

    system_message_template = Template(
        """
You are an excellent java developer focused on updating dependencies in a maven `pom.xml` file.
You are overseeing a migration effort of a Java application in which we have encountered a maven issue.
Help fix the given problem by adding a new dependency to the pom file.
Follow the given guidelines and make use of the functions described to you to make an educated decision of which dependency to add or update.
{% if background %}
Here is the original migration issue we were trying to fix that led to this new issue in maven. Make sure that the dependency you add or update aligns with the migration goal.
{{ background }}
{% endif %}
### Guidelines:
1. Only use the provided and predefined functions as the functions. Do not use any other functions.
2. Always search for the fqdn for the dependency to be added or updated.
3. Carefully think through the actions needed before responding.

### Functions:
   ```
1. **Searching  For Full Dependency Fully Qualified Domain Name**:
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
1 We must always use an exact version from the search for Fully Qualified Domain Name of the dependency that we want to add or update.
2 search_fqdn: use this tool to get the fully qualified domain name of a dependency. This includes the artifactId, groupId and the version.
"""
    )

    few_shot_examples = [
        HumanMessage(
            content="""Given the message, you should determine the dependency that needs to be changed.

You must use the following format:

Thought: You should always think about what to do based on the guidelines
Action: The action as block of code to take
Observation: Output what the goal of the action is achieving

Issue:

package org.apache.commons.io does not exist
"""
        ),
        AIMessage(
            content="""Thought: The error message indicates that the package `org.apache.commons.io` does not exist. This suggests that the dependency for Apache Commons IO might be missing or incorrectly specified in the `pom.xml` file. I need to find the correct dependency for Apache Commons IO and update the `pom.xml` file accordingly.

Action:
```python
result = search_fqdn.run(artifact_id="commons-io", group_id="org.apache.commons")
```

Observation: This action will provide the fully qualified domain name, including the latest version, for the SmallRye Reactive Messaging dependency."""
        ),
    ]

    inst_msg_template = HumanMessagePromptTemplate.from_template(
        """
Given the message, you should determine the dependency that needs to be changed.

You must use the following format:

Thought: You should always think about what to do based on the guidelines
Action: The action as block of code to take
Observation: Output what the goal of the action is achieving

Issue:

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
        retries: int = 2,
    ) -> None:
        self._model_provider = model_provider
        self._max_retries = retries
        self.child_agent = FQDNDependencySelectorAgent(model_provider=model_provider)
        self.agent_methods.update({"find_in_pom._run": find_in_pom(project_base)})

    def execute(self, ask: AgentRequest) -> AgentResult:
        if not isinstance(ask, MavenDependencyRequest):
            return AgentResult()

        request: MavenDependencyRequest = ask

        if not request.message:
            return AgentResult()

        system_message = SystemMessage(
            content=self.system_message_template.render(background=ask.background)
        )

        instruction_msg = self.inst_msg_template.format(message=request.message)

        msg: list[BaseMessage] = [system_message]
        msg.extend(self.few_shot_examples)
        msg.append(instruction_msg)
        fix_gen_attempts = 0
        llm_response: Optional[_llm_response] = None
        initial_maven_search: Union[FQDNResponse, list[FQDNResponse], None] = None

        # TODO: shawn-hurley: this is needs to be different to allow for the sub-agent's that are needed.
        # We need a sub-agent in the case when searching for the fqdn does not return a single result or
        # no result. In this case we will want the sub agent to try and give us additional information.
        # Today, if we don't have the FQDN then we are going to skip updating for now.

        all_actions: list[_action] = []
        while fix_gen_attempts < self._max_retries:
            fix_gen_attempts += 1

            fix_gen_response = self._model_provider.invoke(
                msg, cache_path_resolver=ask.cache_path_resolver
            )
            llm_response = self.parse_llm_response(fix_gen_response.content)

            # we have to keep the chat going until we get a final answer
            msg.append(AIMessage(content=fix_gen_response.content))

            if llm_response is None or not llm_response.actions:
                msg.append(
                    HumanMessage(
                        content="Please provide a complete response and use the given functions exactly as described to search for dependency."
                    )
                )
                continue

            all_actions.extend(llm_response.actions)
            for action in llm_response.actions:
                for method_name, method in self.agent_methods.items():
                    if method_name in action.code:
                        if callable(method):
                            method_out = method(action.code)
                            if isinstance(method_out, FQDNResponse) or (
                                isinstance(method_out, list)
                                and all(
                                    isinstance(item, FQDNResponse)
                                    for item in method_out
                                )
                            ):
                                initial_maven_search = method_out
                                break

            # initial maven search is all we need to add the dep
            if initial_maven_search:
                break

            msg.append(
                HumanMessage(
                    content="No FQDNs found with the given group and artifact."
                )
            )

        if llm_response is None or fix_gen_response is None:
            return AgentResult()

        maven_search: Optional[FQDNResponse] = None

        # we found the answer in initial search, no need to go to the fqdn selection part
        if isinstance(initial_maven_search, FQDNResponse):
            maven_search = initial_maven_search

        if not initial_maven_search or isinstance(initial_maven_search, list):
            for a in all_actions:
                if "search_fqdn.run" in a.code:
                    logger.info("Need to call sub-agent for selecting FQDN")
                    r = self.child_agent.execute(
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

        # We are going to give back the response, The caller should be responsible for running the code generated by the AI.
        # If we have not take the actions step wise, in the LLM, we need to run all but editor here
        # and give that information to the caller.
        return MavenDependencyResult(
            encountered_errors=None,
            fqdn_response=maven_search,
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
