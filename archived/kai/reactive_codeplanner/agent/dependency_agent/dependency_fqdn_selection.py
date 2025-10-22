from dataclasses import dataclass
from typing import Any, Optional

from jinja2 import Template
from langchain_core.messages import HumanMessage, SystemMessage

from kai.llm_interfacing.model_provider import ModelProvider
from kai.logging.logging import get_logger
from kai.reactive_codeplanner.agent.api import Agent, AgentRequest, AgentResult
from kai.reactive_codeplanner.agent.dependency_agent.api import FQDNResponse
from kai.reactive_codeplanner.agent.dependency_agent.util import (
    get_maven_query,
    get_maven_query_from_code,
    search_fqdn_query,
)
from kai.rpc_server.chat import get_chatter_contextvar

logger = get_logger(__name__)
chatter = get_chatter_contextvar()


@dataclass
class FQDNDependencySelectorRequest(AgentRequest):
    msg: str
    code: str
    query: list[str]
    times: int

    def from_selector_request(
        ask: "FQDNDependencySelectorRequest", new_query: list[str]
    ) -> "FQDNDependencySelectorRequest":
        """Will create a new selector request bumping the times by one"""
        req = FQDNDependencySelectorRequest(
            ask.file_path,
            msg=ask.msg,
            code="",
            query=new_query,
            times=ask.times + 1,
            task=ask.task,
            background=ask.background,
        )
        req.cache_path_resolver = ask.cache_path_resolver
        return req


@dataclass
class FQDNDependencySelectorResult(AgentResult):
    response: FQDNResponse | list[FQDNResponse] | None = None


class FQDNDependencySelectorAgent(Agent):
    @dataclass
    class __llm_response:
        artifact_id: str
        group_id: str
        reasoning: str

    def __init__(self, model_provider: ModelProvider) -> None:
        self._model_provider = model_provider

    system_tmpl = Template(
        """
Given an initial Maven compiler and a list of attempted searches, provide an updated dependency to use.
Do not use a dependency that has already been tried.
Only after all the dependencies have been tried, say only the word "TERMINATE", wait for the list of tried dependencies to have all the tries.
                       
Think through the problem. But only give one dependency to try at a time. You should only output "TERMINATE" or in the following format:

Reasoning

ArtifactId:
GroupId:
"""
    )
    message = Template(
        """
{{message}}

Searched dependencies:
{% for q in query %}
{{q}}
{% endfor %}
"""
    )

    async def execute(self, ask: AgentRequest) -> FQDNDependencySelectorResult:
        await chatter.get().chat_simple("FQDNDependencySelectorAgent executing...")

        if not isinstance(ask, FQDNDependencySelectorRequest):
            return FQDNDependencySelectorResult(
                encountered_errors=None, file_to_modify=None, response=None
            )

        query = ask.query
        if ask.code:
            query = []
            query.append(get_maven_query_from_code(ask.code))

        msg = [
            SystemMessage(content=self.system_tmpl.render()),
            HumanMessage(content=self.message.render(message=ask.msg, query=query)),
        ]
        fix_gen_response = await self._model_provider.ainvoke(
            msg, ask.cache_path_resolver
        )
        llm_response = self.parse_llm_response(fix_gen_response.content)
        # Really we need to re-call the agent
        if not llm_response:
            return FQDNDependencySelectorResult(
                encountered_errors=None, file_to_modify=None, response=None
            )

        new_query = get_maven_query(
            artifact_id=llm_response.artifact_id, group_id=llm_response.group_id
        )
        response = search_fqdn_query(new_query)
        logger.debug("got response: %s from searching FQDN", response)
        ## only run this 5 times
        if (not response or isinstance(response, list)) and ask.times < 5:
            ## need to recursively call execute.
            query.append(new_query)
            return await self.execute(
                FQDNDependencySelectorRequest.from_selector_request(ask, query)
            )
        if isinstance(response, list):
            response = None
        return FQDNDependencySelectorResult(
            encountered_errors=None, file_to_modify=None, response=response
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
        if "TERMINATE" in content:
            return None
        for line in content.splitlines():
            if not line:
                continue
            elif "ArtifactId:" in line:
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
            elif "Reasoning:" in line or in_reasoning:
                in_reasoning = True
                reasoning_str = "\n".join([reasoning_str, line])

        return self.__llm_response(
            artifact_id=artifact_id, group_id=group_id, reasoning=reasoning_str
        )
