import os
from dataclasses import dataclass
from urllib.parse import unquote, urlparse

from git import Repo

from kai.models.kai_config import KaiConfigIncidentStoreInMemoryArgs
from kai.report import Report

from .incident_store import Application, IncidentStore, Solution


# These classes are just for the in-memory data store. Once we figure out the
# best way to model the incidents, violations, etc... we can remove these
@dataclass(frozen=True)
class InMemoryIncident:
    uri: str
    snip: str
    line: int
    variables: dict


@dataclass(frozen=True)
class InMemorySolvedIncident:
    uri: str
    snip: str
    line: int
    variables: dict
    file_diff: str
    repo_diff: str
    original_code: str
    updated_code: str


@dataclass
class InMemoryViolation:
    unsolved_incidents: list[InMemoryIncident]
    solved_incidents: list[InMemorySolvedIncident]


@dataclass
class InMemoryRuleset:
    violations: dict[str, InMemoryViolation]


@dataclass
class InMemoryApplication:
    current_commit: str
    rulesets: dict[str, InMemoryRuleset]


class InMemoryIncidentStore(IncidentStore):
    def __init__(self, args: KaiConfigIncidentStoreInMemoryArgs):
        self.store: dict[str, InMemoryApplication] = {}

    def delete_store(self):
        self.store = {}

    def load_report(self, app: Application, report: Report) -> tuple[int, int, int]:
        """
        Returns: (number_new_incidents, number_unsolved_incidents,
        number_solved_incidents): tuple[int, int, int]
        """
        # FIXME: Only does stuff within the same application. Maybe fixed?

        # create entries if not exists
        # reference the old-new matrix
        #           old
        #         | NO     | YES
        # --------|--------+-----------------------------
        # new NO  | -      | update (SOLVED, embeddings)
        #     YES | insert | update (line number, etc...)

        repo_path = unquote(urlparse(app.repo_uri_local).path)
        repo = Repo(repo_path)
        old_commit: str
        new_commit = app.current_commit

        number_new_incidents = 0
        number_unsolved_incidents = 0
        number_solved_incidents = 0

        application = self.store.setdefault(
            app.application_name, InMemoryApplication(app.current_commit, {})
        )

        old_commit = application.current_commit
        report_dict = report.get_report()

        number_new_incidents = 0
        number_unsolved_incidents = 0
        number_solved_incidents = 0

        for ruleset_name, ruleset_dict in report_dict.items():
            ruleset = application.rulesets.setdefault(ruleset_name, InMemoryRuleset({}))

            for violation_name, violation_dict in ruleset_dict.get(
                "violations", {}
            ).items():
                violation = ruleset.violations.setdefault(
                    violation_name, InMemoryViolation({})
                )

                store_incidents = set(violation.unsolved_incidents)
                report_incidents = set(
                    InMemoryIncident(
                        x.get("uri", ""),
                        x.get("codeSnip", ""),
                        x.get("lineNumber", 0),
                        x.get("variables", {}),
                    )
                    for x in violation_dict.get("incidents", [])
                )

                new_incidents = report_incidents.difference(store_incidents)
                number_new_incidents += len(new_incidents)
                for incident in new_incidents:
                    violation.unsolved_incidents.append(incident)

                unsolved_incidents = report_incidents.intersection(store_incidents)
                number_unsolved_incidents += len(unsolved_incidents)

                solved_incidents = store_incidents.difference(report_incidents)
                number_solved_incidents += len(solved_incidents)
                for incident in solved_incidents:
                    file_path = os.path.join(
                        repo_path,
                        unquote(urlparse(incident.uri).path).removeprefix(
                            "/tmp/source-code/"
                        ),
                    )

                    try:
                        original_code = repo.git.show(f"{old_commit}:{file_path}")
                    except Exception:
                        original_code = ""

                    try:
                        updated_code = repo.git.show(f"{new_commit}:{file_path}")
                    except Exception:
                        updated_code = ""

                    repo_diff = repo.git.diff(old_commit, new_commit)
                    file_diff = repo.git.diff(old_commit, new_commit, "--", file_path)

                    violation.solved_incidents.append(
                        InMemorySolvedIncident(
                            uri=incident.uri,
                            snip=incident.snip,
                            line=incident.line,
                            variables=incident.variables,
                            original_code=original_code,
                            updated_code=updated_code,
                            file_diff=file_diff,
                            repo_diff=repo_diff,
                        )
                    )

        return number_new_incidents, number_unsolved_incidents, number_solved_incidents

    def find_solutions(
        self,
        ruleset_name: str,
        violation_name: str,
        incident_variables: dict,
        incident_snip: str | None = None,
    ) -> list[Solution]:
        result: list[Solution] = []
        incident_variables_set = set(incident_variables.items())
        incident_variables_set_len = len(incident_variables_set)

        for _, application in self.store.items():
            ruleset = application.rulesets.get(ruleset_name, None)
            if ruleset is None:
                continue

            violation = ruleset.violations.get(violation_name, None)
            if violation is None:
                continue

            for solved_incident in violation.solved_incidents:
                if incident_snip != None and solved_incident.snip != incident_snip:
                    continue

                common = set(solved_incident.variables.items()).intersection(
                    incident_variables_set
                )
                if len(common) != incident_variables_set_len:
                    continue

                result.append(
                    Solution(
                        solved_incident.uri,
                        solved_incident.file_diff,
                        solved_incident.repo_diff,
                        solved_incident.original_code,
                        solved_incident.updated_code,
                    )
                )

        return result
