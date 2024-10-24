from dataclasses import dataclass
from typing import Any, Optional

from jinja2 import Template
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage

from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.api import Agent, AgentRequest, AgentResult
from kai.reactive_codeplanner.agent.dependency_agent.api import FQDNResponse
from kai.reactive_codeplanner.agent.dependency_agent.util import (
    get_maven_query,
    get_maven_query_from_code,
    search_fqdn_query,
)

logger = get_logger(__name__)


@dataclass
class FQDNDependencySelectorRequest(AgentRequest):
    msg: str
    code: str
    query: list[str]
    times: int


@dataclass
class FQDNDependencySelectorResult(AgentResult):
    response: FQDNResponse | list[FQDNResponse] | None


class FQDNDependencySelectorAgent(Agent):
    @dataclass
    class __llm_response:
        artifact_id: str
        group_id: str
        reasoning: str

    def __init__(self, llm: BaseChatModel) -> None:
        self.__llm = llm

    message = Template(
        """
You are an excellent Java developer with expertise in dependency management.

Given an initial Maven compiler and a list of attempted searchs, provide an updated dependency to use.
Do not use a dependency that has already been tried.
                       
Think through the problem fully. Do not update the dependency if it has moved to newer versions; we want to find the version that matches, regardless of whether it is old or not. 

Output in the format of:

Reasoning

ArtifactId:
GroupId:

{{message}}

Searched dependencies:
{% for q in query %}
{{q}}
{% endfor %}
"""
    )

    def execute(self, ask: AgentRequest) -> FQDNDependencySelectorResult:
        if not isinstance(ask, FQDNDependencySelectorRequest):
            return FQDNDependencySelectorResult(
                encountered_errors=None, modified_files=None, response=None
            )

        query = ask.query
        if ask.code:
            query = []
            query.append(get_maven_query_from_code(ask.code))

        msg = [HumanMessage(content=self.message.render(message=ask.msg, query=query))]
        fix_gen_response = self.__llm.invoke(msg)
        llm_response = self.parse_llm_response(fix_gen_response.content)
        # Really we need to re-call the agent
        if not llm_response:
            return FQDNDependencySelectorResult(
                encountered_errors=None, modified_files=None, response=None
            )

        new_query = get_maven_query(
            artifact_id=llm_response.artifact_id, group_id=llm_response.group_id
        )
        response = search_fqdn_query(new_query)
        logger.debug("got response: %r from searchign FQDN")
        ## only run this 5 times
        if (not response or isinstance(response, list)) and ask.times < 5:
            ## need to recursively call execute.
            query.append(new_query)
            return self.execute(
                FQDNDependencySelectorRequest(
                    ask.file_path,
                    msg=ask.msg,
                    code="",
                    query=query,
                    times=ask.times + 1,
                )
            )
        if isinstance(response, list):
            response = None
        return FQDNDependencySelectorResult(
            encountered_errors=None, modified_files=None, response=response
        )

    def parse_llm_response(
        self, content: str | list[str | dict[Any, Any]]
    ) -> Optional[__llm_response]:
        if isinstance(content, dict) or isinstance(content, list):
            return None

        in_reasoning = False
        reasoning_str = ""
        artifact_id = ""
        group_id = ""
        for line in content.splitlines():
            if not line:
                continue
            elif "ArtifactId" in line:
                # Get the line
                parts = line.split(":")
                if len(parts) != 2:
                    logger.error("invalid parts: %r", parts)
                artifact_id = parts[1].strip()
            elif "GroupId:" in line:
                parts = line.split(":")
                if len(parts) != 2:
                    logger.error("invalid parts: %r", parts)
                group_id = parts[1].strip()
                pass
            elif "Reasoning" in line or in_reasoning:
                in_reasoning = True
                reasoning_str = "\n".join([reasoning_str, line])

        return self.__llm_response(
            artifact_id=artifact_id, group_id=group_id, reasoning=reasoning_str
        )
