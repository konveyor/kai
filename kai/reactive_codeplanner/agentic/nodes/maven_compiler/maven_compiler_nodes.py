from langchain.tools.render import render_text_description
from langchain_core.messages import HumanMessage

from kai.cache import CachePathResolver
from kai.llm_interfacing.model_provider import ModelProvider
from kai.reactive_codeplanner.agentic.schemas.maven_compiler.schema import (
    InitState,
    State,
)
from kai.reactive_codeplanner.agentic.tools.base import KaiBaseTool
from kai.reactive_codeplanner.task_runner.compiler.maven_validator import (
    PackageDoesNotExistError,
)


class NoTaskFoundError(Exception):
    pass


class InvalidTask(Exception):
    pass


class MavenCompilerNodes:

    def __init__(
        self,
        model: ModelProvider,
        cache_path_resolver: CachePathResolver,
        tools: list[KaiBaseTool],
    ) -> None:
        self.model = model
        self.cache_path_resolver = cache_path_resolver
        self.tools = tools

    async def handle_dependency_missing_task(self, state: InitState) -> InitState:
        """This will take the given Package Not Found error, and the pom.xml and determine where it should look for the dependency"""

        if not state.task:
            raise NoTaskFoundError(f"unable to get task from state - {state}")

        if not isinstance(state.task, PackageDoesNotExistError):
            raise InvalidTask(
                f"{self.__class__} can only work on {PackageDoesNotExistError} errors found {state.task.__class__}"
            )

        background = state.background
        if not background:
            background = f"none"

        with open(state.file_path) as f:
            source_file = f.read()

        prompt = f"""
I will give you a pom.xml file for which I want to use to solve the compilations errors.

The context that you are working in is a migration, and the prior steps taken are {background}.

I will provide you with the maven compiler errors highlighting the issues wich need to be addressed.

Use the given tools as needed to gather more information.

Once you have determined the correct fix for the compilation error you should print out the step by step instructions to do so.

If you want to update any code, please put it in a code block like:

```xml -- <path to file to update>
    <dependency>
        <artifactId>placeholder</artifactId>
        <groupId>placeholder</groupId</groupId>
        <version>placeholder</version>
    </dependency>
```

You may conisder looking for the dependencies that are availble to you. 
You may conisder finding a task that will add a build of materials to the pom file adding that, and then getting all the dependencies.

Source File:
{source_file}

Compiler Errors:
{state.task.compiler_error_message()}
"""

        ai_message = await self.model.ainvoke(
            [HumanMessage(content=prompt)],
            self.cache_path_resolver,
        )

        return state
