# TODO: Come up with some sort of "solution generator strategy" so we
# don't blow up our llm API usage. Lazy, immediate, other etc...

import enum
import os
from abc import ABC, abstractmethod
from urllib.parse import unquote, urlparse

from git import Repo

from kai.model_provider import ModelProvider
from kai.service.incident_store.incident_store import (
    Solution,
    SQLIncident,
    remove_known_prefixes,
)


class SolutionProducerKind(enum.Enum):
    TEXT_ONLY = "text_only"
    LLM_LAZY = "llm_lazy"


class SolutionProducer(ABC):
    @abstractmethod
    def produce_one(
        self, incident: SQLIncident, repo: Repo, old_commit: str, new_commit: str
    ) -> Solution:
        pass

    def produce_many(
        self, incidents: list[SQLIncident], repo: Repo, old_commit: str, new_commit: str
    ) -> list[Solution]:
        return [
            self.produce_one(incident, repo, old_commit, new_commit)
            for incident in incidents
        ]


class SolutionProducerTextOnly(SolutionProducer):
    def produce_one(
        self, incidents: SQLIncident, repo: Repo, old_commit: str, new_commit: str
    ) -> Solution:
        solutions: list[Solution] = []

        for incident in incidents:
            file_path = os.path.join(
                repo.working_tree_dir,
                remove_known_prefixes(unquote(urlparse(incident.file_path).path)),
            )

            # NOTE: `repo_diff` functionality is not implemented

            # TODO: Some of the sample repos have invalid utf-8 characters,
            # thus the encode-then-decode hack. Not very performant, there's
            # probably a better way to handle this.
            try:
                original_code = (
                    repo.git.show(f"{new_commit}:{file_path}")
                    .encode("utf-8")
                    .decode("utf-8")
                )
            except Exception:
                original_code = ""

            try:
                updated_code = (
                    repo.git.show(f"{new_commit}:{file_path}")
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

            solutions.append(
                Solution(
                    uri=incident.incident_uri,
                    file_diff=file_diff,
                    original_code=original_code,
                    updated_code=updated_code,
                )
            )

        return solutions


class SolutionProducerLLMLazy(SolutionProducer):
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider

    def produce_many(
        self, incidents: SQLIncident, repo: Repo, old_commit: str, new_commit: str
    ) -> Solution:
        solutions = SolutionProducerTextOnly().produce_many(
            incidents, repo, old_commit, new_commit
        )

        for solution in solutions:
            solution.llm_summary_generated = False

        return solutions
