
import sys

sys.modules['_elementtree'] = None
import json
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import requests
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from playpen.repo_level_awareness.agent.api import Agent, AgentRequest, AgentResult
from playpen.repo_level_awareness.utils.xml import LineNumberingParser


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
class FQDNResponse:
    artifact_id: str
    group_id: str
    version: str

    def to_llm_message(self) -> HumanMessage:
        return HumanMessage(f"the result is {json.dumps(self.__dict__)}")

@dataclass
class FindInPomResponse:
    start_line: int
    end_line: int

    def to_llm_message(self) -> HumanMessage:
        return HumanMessage(f"the start_line is {self.start_line} and end_line is {self.end_line}")

@dataclass
class MavenDependencyResult(AgentResult):
    final_answer: str
    fqdn_response: FQDNResponse
    find_in_pom: FindInPomResponse

@dataclass
class _llm_response():
    actions: List[_action]
    final_answer: str

def search_fqdn(code: str) -> FQDNResponse:
    query = get_maven_query(code)
    resp = requests.get(f"https://search.maven.org/solrsearch/select?q={query}")
    if resp.status_code != 200:
        return FQDNResponse(artifact_id="", group_id="", version="")
    o = resp.json()
    docs = o['response']['docs']
    if not docs:
        return FQDNResponse(artifact_id="", group_id="", version="")
    if len(docs) > 1:
        ### Here, I think we need to have a specific return, that then asks the LLM to chose which one based on the
        ### context.
        
        return FQDNResponse(artifact_id="", group_id="", version="")
    else: 
        d = docs[0]
        return FQDNResponse(artifact_id= d['a'], group_id=d['g'], version=d['latestVersion'])

def get_maven_query(code: str) -> str:
    # We need to remove the function call information from the code.
    start_i = code.index("(")
    end_i = code.index(")")

    # Need to remove the not needed chars, whitespace and '"' and ()
    o = code[start_i:end_i].strip()
    
    parts = o.split(",")
    kwargs = {}

    for p in parts:
        args = p.split("=")
        kwargs[args[0].strip().strip('""()')] = args[1].strip().strip('""')

    #fmt: off
    query = []
    if "artifact_id" in kwargs:
        query.append(f"a:{kwargs["artifact_id"]}")
    if "group_id" in kwargs:
        query.append(f"g:{kwargs["group_id"]}")
    if "version" in kwargs:
        query.append(f"v:{kwargs["version"]}")
    return " AND ".join(query)
    #fmt: on

def find_in_pom(path: Path) -> Callable:
    ## Open XML file
    ## parse XML, find the dependency node if we have group and artifact we will return start_line and end_line for the full node
    ## If we don't have group and artifact, but we have dependencies, then we will find the start of the dependecies node. start_line and end_line will be the same. The start of the dependencies.
    tagToKwargs = {
        "{http://maven.apache.org/POM/4.0.0}artifactId": "artifactId",
        "{http://maven.apache.org/POM/4.0.0}groupId": "groupId"
    }
    def f(code: str) -> FindInPomResponse:
        i = code.index("keywords")
        # Remove 8 chars to get ride of keyword=
        s = code[i+9:].strip('(){}')
        parts = s.split(",")
        kwargs = {}
        for p in parts:
            v = p.split(":")
            kwargs[v[0].strip(' ""')]= v[1].strip(' ""').strip()
        
        tree = ET.parse(os.path.join(path, "pom.xml"), parser=LineNumberingParser())
        root = tree.getroot()
        dep = root.find('{http://maven.apache.org/POM/4.0.0}dependencies')
        deps = root.findall('*//{http://maven.apache.org/POM/4.0.0}dependency')
        for d in deps:
            found = []
            for c in d:
                key = tagToKwargs.get(c.tag)
                if not key:
                    continue
                v = kwargs[key]
                if c.text == v:
                    found.append(True)
            if len(found) == 2:
                return FindInPomResponse(d._start_line_number, d._end_line_number)
        return FindInPomResponse(dep._start_line_number, dep._start_line_number)
    return f


class MavenDependencyAgent(Agent):

    sys_msg=SystemMessage("""
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
   - version: Optinal[str] - The line number where the alias is used.
   Action:
   ```python
   result = search_fqdn.run(artificat_id="commons-collections4", group_id="org.apache.commons", version="4.5.0-M2")
   print(result)
   ```

### Important Notes:
1 We must always use an exact version from the search for Fully Qualified Domain Name of the dependency that we want to update
3. search_fqdn: use this tool to get the fully qualified domain name of a dependecy. This includes the artificatId, groupId and the version.

Use this tool to get all references to a symbol in the codebase. This will help you understand how the symbol is used in the codebase. For example, if you want to know where a function is called, you can use this tool.


### Example:
Thought: replace com.google.guava/guava with org.apache.commons/commons-collections4 to the latest version.


Thought:  I have the groupId and the artificatId for the collections4 library, but I don't have the latest version.
Action: ```python
result = search_fqdn.run(artificat_id="commons-collections4", group_id="org.apache.commons")
```
Observation: We now have the fqdn for the commons-collections4 dependency

Though: Now I have the latest version information I need to find the where guava is in the file to replace it.
Action: ```python
start_line, end_line = find_in_pom._run(relative_file_path="module/file.py", keywords={"groupId": "com.google.guava"", "artifactId": "guava")
```
Observation: we now have the start and end line of the in the pom file to be updated

Thought: Now that I have the latest version information and the current start_line and end_line I need to replace the dependency
Action: ```python
  xml =  f"<dependency><groupId>{result.groupjId}</groupId><artifactId>{result.artifactId}</artifactId><version>{result.version}</version></dependency>"
   result = editor._run(relative_file_path="pom.xml", start_line=start_line, end_line=end_line, patch=xml)
   print(result)
Observation: The pom.xml file is now updatedd setting the xml at start line with the new dependency to the end line

Final Answer:
Updated the guava to the commons-collections4 dependency
    """)

    inst_msg_template = HumanMessagePromptTemplate.from_template("""
[INST]
Given the message, you should determine the dependency that needs to be changed.

You must use the following format:

Thought: you should always think about what to do based on the guidelines
Action: the action as block of code to take
Observation: output what the goal of the action is achieving 

When completed, add Final Answer that tells the steps taken


If you are at the point of editing, add the final answer of what you did

Message:{message}
    """)

    agent_methods = {"search_fqdn.run": search_fqdn, 
                     "find_in_pom.run": find_in_pom
                     }

    def __init__(
        self,
        llm: BaseChatModel,
        project_base: Path,
        retries: int = 1,
    ) -> None:
        self.__llm = llm
        self._retries = retries
        self.agent_methods.update({"find_in_pom.run": find_in_pom(project_base)})
    

    def execute(self, ask: AgentRequest) -> MavenDependencyResult:
        if not isinstance(ask, MavenDependencyRequest):
            return AgentResult(encountered_errors=[], modified_files=[])

        t: MavenDependencyRequest= ask

        if not t.message :
            return AgentResult(None, None)

        msg = [self.sys_msg, self.inst_msg_template.format(message=t.message)]
        fix_gen_attempts = 0
        llm_response: Optional[_llm_response] = None
        maven_search: FQDNResponse = None
        find_pom_lines: FindInPomResponse = None
        
        #TODO: shawn-hurley: this is needs to be different to allow for the sub-agent's that are needed. 
        # We need a sub-agent in the case when searching for the fqdn does not return a single result or
        # no result. In this case we will want the sub agent to try and give us additional information.
        # Today, if we don't have the FQDN then we are going to skip updating for now.

        while fix_gen_attempts < self._retries: 
            fix_gen_attempts += 1

            fix_gen_response = self.__llm.invoke(msg)
            llm_response = self.parse_llm_response(
                fix_gen_response.content
            )
            print(llm_response)
            # Break out of the while loop, if we don't have a final answer then we need to retry
            if not self.__should_continue(llm_response): 
                break

            # We do not believe that we should not conintue now we have to continue after running the code that is asked to be run.
            # The only exception to this rule, is when we actually update the file, that should be handled by the caller.
            # This happens sometimes that the LLM will stop and wait for more information. 

            for a in llm_response.actions:
                for s, method in self.agent_methods:
                    if s in a.code:
                        print(method)
                        method_out = method(a.code)
                        a = getattr(method_out, "to_llm_message", None)
                        if callable(a):
                            msg.append(method_out.to_llm_message())
                            print(msg)
            
            self._retries += 1

        if llm_response is None or fix_gen_response is None:
            return AgentResult(encountered_errors=[], modified_files=[])

        if not maven_search:
            for a in llm_response.actions:
                if "search_fqdn.run" in a.code:
                    m = self.agent_methods.get("search_fqdn.run")
                    print(m)
                    maven_search= m(a.code)
        
        if not find_pom_lines:
            for a in llm_response.actions:
                if "find_in_pom.run" in a.code:
                    m = self.agent_methods.get("find_in_pom.run")
                    print(m)
                    find_pom_lines= m(a.code)



        # We are going to give back the response, The caller should be responsible for running the code generated by the AI.      
        # If we have not take the actions step wise, in the LLM, we need to run all but editor here
        # and give that information to the caller.
        return MavenDependencyResult(encountered_errors=None, 
                                     modified_files=None, 
                                     final_answer=llm_response.final_answer,
                                     fqdn_response=maven_search,
                                     find_in_pom=find_pom_lines)

    def parse_llm_response(self, content: str | List[str] | Dict) -> Optional[_llm_response]:
        # We should not expect that the value is anything other than str for the type of 
        # call that we know we are making
        if isinstance(content, Dict) or isinstance(content, List):
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
            if not line.strip().strip("```") or line == "```python":
                continue

            parts = line.split(":")
            
            if len(parts) > 1 :
                match parts[0]:
                    case "Thought":
                        s = ":".join(parts[1:])
                        if code_block or observation_str:
                            actions.append(_action(code_block, thought_str, observation_str))
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
                        actions.append(_action(code_block, thought_str, observation_str))
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
                    observation_str= "\n".join([observation_str, line]).strip()
                else:
                    observation_str = line.strip()
        return _llm_response(actions, final_answer)

    def __should_continue(self, llm_response: Optional[_llm_response]) -> bool:
        print(llm_response)
        if not llm_response or not llm_response.final_answer:
            return True
        return False
        


            
                
                

            


            
