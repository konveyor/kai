import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from langchain.prompts.chat import (
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.messages import AIMessage, HumanMessage

from kai.llm_interfacing.model_provider import ModelProvider
from kai.logging.logging import TRACE, get_logger
from kai.reactive_codeplanner.agent.api import Agent, AgentRequest, AgentResult
from kai.reactive_codeplanner.agent.ast_diff.parser import Language, extract_ast_info

logger = get_logger(__name__)


@dataclass
class ReflectionTask(AgentRequest):
    # contents of input file prior to invoking previous agent
    original_file_contents: str
    # contents of updated file produced by previous agent
    updated_file_contents: str
    # a list of issues originally identified in the file
    issues: list[str]
    # reasoning produced by previous agent
    reasoning: str = ""
    # a keyword describing target technology to act as a hint to agent
    target_technology: str = ""
    # keyword describing overall application's language
    app_language: str = "Java"


class ReflectionAgent(Agent):
    """Reflection agent reflects on LLM responses of different agents"""

    msg_templ_sys_reflect = SystemMessagePromptTemplate.from_template(
        """You are a senior engineer with extensive experience in developing enterprise {app_language} applications.
You are helping migrate old {app_language} applications to a newer technology.
A junior engineer has updated a {source_file_language} file in an application to migrate it to a newer technology.
Use your best judgement to analyze the input data and review the changes.
"""
    )

    msg_templ_sys_fix = SystemMessagePromptTemplate.from_template(
        """You are a senior engineer well versed in {app_language}.
You have extensive experience in migrating enterprise {app_language} applications to newer technologies.
You are overseeing a migration of an enterprise {app_language} application to {target_technology}.
You will be given an input file, and a list of migration issues identified in the file.
Fix all the issues described and generate an updated file.
"""
    )

    msg_templ_user_reflect = HumanMessagePromptTemplate.from_template(
        """You will be given a list of migration issues found in an old {source_file_language} file in JSON format.
Instead of the {source_file_language} files themselves, you will be given a difference between old file and the new file in JSON format.
The difference is constructed by comparing ASTs of the two files. The JSON keys are self-explanatory.

You will analyze the differences expressed in JSON format to create a mental picture of the old source code and the new.
You will compare the analyzed data with the list of issues and identify which of the issues are not fixed.
Issues often describe the expected change that needs to happen. You will use your best judgement to identify whether the issue is fixed as described.
You will also look for any new changes that were not originally mentioned in the issues.
You will also spot any changes that suggest a change in the original functionality.
If you find an issue that's not fixed, briefly describe why you think the issue is not fixed in 1-2 lines. If you find unnecessary changes, point those out too.
Be precise in pointing out issues that are not fixed.
If you find the changes satisfactory, clearly output the word "TERMINATE" in your response.

## Issues identified in the input file

{issues}

## Differences in ASTs of both files

{diff}
"""
    )

    msg_templ_user_reflect_no_diff = HumanMessagePromptTemplate.from_template(
        """A junior engineer has updated a {source_file_language} file in order to migrate it to a newer technology.
The updated file usually updates the original file to make it suitable for the newer technology.
However, it sometimes only contains only the change and not the whole file.
Use your best judgement to understand if the migrated file is complete and does not omit other content from original file.
It is not important what changes are made but the file has to be complete and valid.
If you find that the file is valid, only output the word "TERMINATE".
If the file is complete and valid, ask the junior engineer to provide a complete file. Do not output the word TERMINATE when file is incomplete or invalid.

## Original File

```
{original_content}
```

## Updated File

```
{updated_content}
```
"""
    )

    no_diff_reflection_solved_examples = [
        msg_templ_user_reflect_no_diff.format(
            source_file_language="xml",
            original_content="""<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>sample-project</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <name>Sample Project</name>
    <url>http://example.com</url>

    <properties>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>javax</groupId>
            <artifactId>javaee-web-api</artifactId>
            <version>7.0</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>
</project>
""",
            updated_content="""<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>sample-project</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <name>Sample Project</name>
    <url>http://example.com</url>

    <properties>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>

    <dependencies>
        <!-- Updated the dependency from javax to jakarta -->
        <dependency>
            <groupId>jakarta.platform</groupId>
            <artifactId>jakarta.jakartaee-api</artifactId>
            <version>8.0.0</version>
            <scope>provided</scope>
         </dependency>
    </dependencies>
</project>
""",
        ),
        AIMessage("The file is complete and valid. TERMINATE."),
        msg_templ_user_reflect_no_diff.format(
            source_file_language="xml",
            original_content="""<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>sample-project</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <name>Sample Project</name>
    <url>http://example.com</url>

    <properties>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>javax</groupId>
            <artifactId>javaee-web-api</artifactId>
            <version>7.0</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>
</project>
""",
            updated_content="""<dependencies>
<!-- Updated the dependency from javax to jakarta -->
    <dependency>
        <groupId>jakarta.platform</groupId>
        <artifactId>jakarta.jakartaee-api</artifactId>
        <version>8.0.0</version>
        <scope>provided</scope>
    </dependency>
</dependencies>
""",
        ),
        AIMessage("Please provide a complete response."),
        msg_templ_user_reflect_no_diff.format(
            source_file_language="java",
            original_content="""package com.example;

import jakarta.ejb.Stateful;
import java.util.ArrayList;
import java.util.List;

@Stateful
public class ShoppingCartBean {
    private List<String> items;

    public ShoppingCartBean() {
        items = new ArrayList<>();
    }

    public void addItem(String item) {
        items.add(item);
    }

    public void removeItem(String item) {
        items.remove(item);
    }

    public List<String> getItems() {
        return items;
    }
}
""",
            updated_content="""package com.example;

import jakarta.enterprise.context.ApplicationScoped;
import java.util.ArrayList;
import java.util.List;

// Updated the @Stateful annotation to @ApplicationScoped
@ApplicationScoped
// rest of the file remains the same
""",
        ),
        AIMessage(
            "The updated file has code omitted and isn't complete. Please provide a complete response."
        ),
    ]

    msg_templ_user_fix = HumanMessagePromptTemplate.from_template(
        """Before attempting to migrate the code to {target_technology} reason through what changes are required and why.
Pay attention to changes you make and impacts to external dependencies in the pom.xml as well as changes to imports we need to consider.
Remember when updating or adding annotations that the class must be imported.
As you make changes that impact the pom.xml or imports, be sure you explain what needs to be updated.
After you have shared your step by step thinking, provide a full output of the updated file. If there are no changes to be made, output the original file as-is.
If you are given a feedback, address all the concerns raised in feedback and respond with an updated file.
Structure your output in Markdown format such as:

## Reasoning
Write the step by step reasoning in this markdown section. If you are unsure of a step or reasoning, clearly state you are unsure and why.

## Updated File
```{source_file_language}
// Write the updated file in this section. Output the entire file.
```
Here's the input information:

## Input file

```{source_file_language}
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

```{source_file_language}
{updated_file}
```
"""
    )

    def __init__(
        self,
        model_provider: ModelProvider,
        iterations: int = 1,
        retries: int = 1,
    ) -> None:
        self._model_provider = model_provider
        self._iterations = iterations
        self._retries = retries

    def execute(self, task: AgentRequest) -> AgentResult:
        if not isinstance(task, ReflectionTask):
            return AgentResult()

        reflection_task: ReflectionTask = task

        _, file_ext = os.path.splitext(reflection_task.file_path)

        language = {
            ".java": Language.Java,
            ".xml": Language.XML,
        }.get(file_ext.lower(), None)

        issues = json.dumps({"issues": list(set(reflection_task.issues))}, indent=4)

        diff = self._get_diff(
            reflection_task.original_file_contents,
            reflection_task.updated_file_contents,
            language,
        )
        if language is None or not reflection_task.issues:
            logger.log(TRACE, "There is nothing to reflect on")
            return AgentResult()

        # initiate chats
        chat_fix_gen = [
            self.msg_templ_sys_fix.format(
                app_language=reflection_task.app_language,
                target_technology=reflection_task.target_technology,
            ),
            self.msg_templ_user_fix.format(
                source_file_language=language,
                input_file=reflection_task.original_file_contents,
                issues=issues,
                target_technology=reflection_task.target_technology,
            ),
            self.msg_templ_ai_fix.format(
                source_file_language=language,
                updated_file=reflection_task.updated_file_contents,
                reasoning=reflection_task.reasoning,
            ),
        ]

        chat_reflect = [
            self.msg_templ_sys_reflect.format(
                app_language=reflection_task.app_language,
                source_file_language=language,
            )
        ]

        # when we couldn't determine diff, we fallback to general reflection
        if not diff:
            chat_reflect.append(
                self.msg_templ_user_reflect_no_diff.format(
                    source_file_language=language,
                    updated_content=reflection_task.updated_file_contents,
                    original_content=reflection_task.original_file_contents,
                    issues=issues,
                )
            )
        else:
            chat_reflect.append(
                self.msg_templ_user_reflect.format(
                    issues=issues,
                    diff=json.dumps(diff, indent=4),
                    source_file_language=language,
                ),
            )

        modified_files = []
        # run agent loop
        curr_iter = 0
        last_updated_file_contents = reflection_task.updated_file_contents
        while curr_iter < self._iterations:
            curr_iter += 1
            try:
                reflection_response = self._model_provider.invoke(
                    chat_reflect,
                    task.cache_path_resolver,
                )
                chat_reflect.append(AIMessage(content=reflection_response.content))
                chat_fix_gen.append(HumanMessage(content=reflection_response.content))
                fix_gen_attempts = 0
                updated_file_contents = None
                fix_gen_response = None
                if "TERMINATE" in reflection_response.content:
                    logger.log(
                        TRACE, "Reflection determined no further changes necessary"
                    )
                    return AgentResult()
                while fix_gen_attempts < self._retries:
                    fix_gen_attempts += 1
                    fix_gen_response = self._model_provider.invoke(
                        chat_fix_gen, task.cache_path_resolver
                    )
                    updated_file_contents = self._parse_llm_response(
                        fix_gen_response.content
                    )
                    if updated_file_contents:
                        break
                if updated_file_contents is None or fix_gen_response is None:
                    logger.log(TRACE, "Invalid reflection response received")
                    return AgentResult()
                last_updated_file_contents = updated_file_contents
                chat_fix_gen.append(AIMessage(content=fix_gen_response.content))
                diff = self._get_diff(
                    last_updated_file_contents, updated_file_contents, language
                )
                if not diff:
                    chat_reflect.append(
                        self.msg_templ_user_reflect_no_diff.format(
                            source_file_language=language,
                            updated_content=reflection_task.updated_file_contents,
                            original_content=reflection_task.original_file_contents,
                            issues=issues,
                        )
                    )
                else:
                    chat_reflect.append(
                        self.msg_templ_user_reflect.format(
                            issues=issues,
                            diff=json.dumps(diff),
                            source_file_language=language,
                        )
                    )
            except Exception as e:
                logger.debug(f"Failed to generate reflection response {str(e)}")
                return AgentResult(encountered_errors=[str(e)])

        # commit the result here
        if last_updated_file_contents:
            modified_files.append(Path(reflection_task.file_path))
            with open(reflection_task.file_path, "w+") as f:
                f.write(last_updated_file_contents)

        return AgentResult(file_to_modify=reflection_task.file_path)

    def _get_diff(
        self, original_content: str, updated_content: str, language: Language | None
    ) -> dict[str, Any]:
        if not language:
            return {}
        try:
            original_file_summary = extract_ast_info(
                original_content, language=language
            )
            updated_file_summary = extract_ast_info(updated_content, language=language)
        except Exception as e:
            logger.error(f"Failed to generate AST diff for reflection - {str(e)}")
            return {}
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

    def _parse_llm_response(
        self, content: str | list[str | dict[Any, Any]]
    ) -> Optional[str]:
        if isinstance(content, list):
            return None
        match_updated_file = re.search(
            r"(?:##|\*\*)\s+[Uu]pdated.*[Ff]ile\s+.*?```\w+\n([\s\S]*?)```",  # trunk-ignore(cspell)
            content,
            re.DOTALL,
        )
        if not match_updated_file:
            return None
        return match_updated_file.group(1).strip()
