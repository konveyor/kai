import os
from abc import ABC, abstractmethod
from urllib.parse import unquote, urlparse

import jinja2
from git import Repo

from kai.constants import PATH_TEMPLATES
from kai.models.file_solution import guess_language
from kai.models.kai_config import SolutionProducerKind
from kai.models.util import remove_known_prefixes
from kai.service.incident_store.sql_types import SQLIncident
from kai.service.llm_interfacing.model_provider import ModelProvider
from kai.service.solution_handling.solution_types import Solution


class SolutionProducer(ABC):
    @abstractmethod
    def produce_one(
        self, incident: SQLIncident, repo: Repo, old_commit: str, new_commit: str
    ) -> Solution:
        """
        Creates a single solution for a single incident. Designed to be called
        right before inserting it into the store.
        """
        pass

    def produce_many(
        self, incidents: list[SQLIncident], repo: Repo, old_commit: str, new_commit: str
    ) -> list[Solution]:
        """
        See `produce_one`.
        """
        return [
            self.produce_one(incident, repo, old_commit, new_commit)
            for incident in incidents
        ]

    @abstractmethod
    def post_process_one(self, incident: SQLIncident, solution: Solution) -> Solution:
        """
        After a solution has been generated, this method performs any additional
        processing needed, deferring any labor-intensive work.

        Think about trying to generated LLM summaries for every single solution
        from the get-go. Not every solution will be used!

        Designed to be called right after selecting an incident from the store.
        """
        pass

    def post_process_many(
        self, incidents: list[SQLIncident], solutions: list[Solution]
    ) -> list[Solution]:
        """
        See `post_process_one`.
        """
        return [
            self.post_process_one(incident, solution)
            for incident, solution in zip(incidents, solutions)
        ]


class SolutionProducerTextOnly(SolutionProducer):
    def produce_one(
        self, incident: SQLIncident, repo: Repo, old_commit: str, new_commit: str
    ) -> Solution:
        local_file_path = remove_known_prefixes(
            unquote(urlparse(incident.incident_uri).path)
        )
        file_path = os.path.join(
            str(repo.working_tree_dir),
            local_file_path,
        )

        # NOTE: `repo_diff` functionality is not implemented

        # TODO: Some of the sample repos have invalid utf-8 characters,
        # thus the encode-then-decode hack. Not very performant, there's
        # probably a better way to handle this.
        try:
            original_code = (
                repo.git.show(f"{old_commit}:{local_file_path}")
                .encode("utf-8")
                .decode("utf-8")
            )
        except Exception:
            original_code = ""

        try:
            updated_code = (
                repo.git.show(f"{new_commit}:{local_file_path}")
                .encode("utf-8")
                .decode("utf-8")
            )
        except Exception:
            updated_code = ""

        file_diff = (
            repo.git.diff(old_commit, new_commit, "--", file_path)
            .encode("utf-8", errors="ignore")
            .decode()
        )

        return Solution(
            uri=incident.incident_uri,
            file_diff=file_diff,
            original_code=original_code,
            updated_code=updated_code,
        )

    def post_process_one(self, incident: SQLIncident, solution: Solution) -> Solution:
        return solution


class SolutionProducerLLMLazy(SolutionProducer):
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider
        self.text_only = SolutionProducerTextOnly()

    def produce_one(
        self, incident: SQLIncident, repo: Repo, old_commit: str, new_commit: str
    ) -> Solution:
        solution = self.text_only.produce_one(incident, repo, old_commit, new_commit)

        solution.llm_summary_generated = False

        return solution

    def post_process_one(self, incident: SQLIncident, solution: Solution) -> Solution:
        if solution.llm_summary_generated:
            return solution

        # Generate the LLM summary to be stored in the solution

        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(PATH_TEMPLATES, "solution_handling")
            ),
            undefined=jinja2.StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )

        template = jinja_env.get_template("generation.jinja")

        # get just the file name and extension from solution.uri
        rendered_template = template.render(
            model_provider=self.model_provider,
            src_file_name=solution.uri,
            src_file_language=guess_language(
                solution.original_code, os.path.basename(solution.uri)
            ),
            src_file_contents=solution.original_code,
            incident={
                "analysis_message": incident.incident_message,
                "line_number": incident.incident_line,
            },
            sln_file_name=solution.uri,
            sln_file_language=guess_language(
                solution.updated_code, os.path.basename(solution.uri)
            ),
            sln_file_contents=solution.updated_code,
        )

        llm_result = self.model_provider.llm.invoke(rendered_template)

        # TODO: Parse LLM result. For now, just returning the content fully

        solution.llm_summary_generated = True
        solution.llm_summary = str(llm_result.content)

        return solution


def solution_producer_factory(
    kind: SolutionProducerKind, model_provider: ModelProvider
):
    # NOTE: Model provider is passed in as a parameter because it's required for
    # the llm stuff. I couldn't figure out a more elegant way of doing this.
    match kind:
        case SolutionProducerKind.TEXT_ONLY:
            return SolutionProducerTextOnly()
        case SolutionProducerKind.LLM_LAZY:
            return SolutionProducerLLMLazy(model_provider)
        case _:
            raise ValueError(f"Unknown solution producer kind: {kind}")
