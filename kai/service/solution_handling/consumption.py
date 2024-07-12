# TODO: Come up with some sort of "solution generator strategy" so we
# don't blow up our llm API usage. Lazy, immediate, other etc...

# FIXME: This should actually be outside of the incident_store. All of this
# functionality should be within the incident production module. This is
# supposed to be more for the llm_io_handler package.

# TODO: Potentially rename this to "SolutionPostProcessor" or "Solution after
# get" or something else that makes more sense. "Consumer" is a bit confusing.
# We could then also trivially add InstructLab generation

import enum
import os
from abc import ABC, abstractmethod

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from kai.constants import PATH_TEMPLATES
from kai.model_provider import ModelProvider
from kai.models.file_solution import guess_language
from kai.service.incident_store.incident_store import Solution, SQLIncident


class SolutionConsumerKind(enum.Enum):
    TEXT_ONLY = "text_only"
    LLM_LAZY = "llm_lazy"


class SolutionConsumer(ABC):
    @abstractmethod
    def consume_one(self, incident: SQLIncident, solution: Solution) -> Solution:
        pass

    def consume_many(
        self, incidents: list[SQLIncident], solutions: list[Solution]
    ) -> list[Solution]:
        return [
            self.consume_one(incident, solution)
            for incident, solution in zip(incidents, solutions, strict=True)
        ]


class SolutionConsumerTextOnly(SolutionConsumer):
    def consume_one(self, incident: SQLIncident, solution: Solution) -> Solution:
        return solution


class SolutionConsumerLLMLazy(SolutionConsumer):
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider

    def consume_one(self, incident: SQLIncident, solution: Solution) -> Solution:
        jinja_env = Environment(
            loader=FileSystemLoader(os.path.join(PATH_TEMPLATES, "solution_handling")),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )

        template = jinja_env.get_template("generation.jinja2")

        # get just the file name and extension from solution.uri
        rendered_template = template.render(
            src_file_name=solution.uri,
            src_file_language=guess_language(
                solution.original_code, os.path.basename(solution.uri)
            ),
            src_file_contents=solution.original_code,
            incident={
                "analysis_message": incident.incident_message,
                "analysis_line_number": incident.incident_line,
            },
            sln_file_name=solution.uri,
            sln_file_language=guess_language(
                solution.updated_code, os.path.basename(solution.uri)
            ),
            sln_file_contents=solution.updated_code,
        )

        llm_result = self.model_provider.llm.invoke(rendered_template)

        # TODO Parse LLM result. For now, just returning the content fully

        solution.llm_summary_generated = True
        solution.llm_summary = llm_result.content

        return solution
