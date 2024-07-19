import json
from dataclasses import dataclass
from typing import Callable

from git import Repo

from kai.models.kai_config import SolutionDetectorKind
from kai.service.incident_store.sql_types import SQLIncident


@dataclass
class SolutionDetectorContext:
    old_incidents: list[SQLIncident]
    new_incidents: list[SQLIncident]
    repo: Repo
    old_commit: str
    new_commit: str


@dataclass
class SolutionDetectorResult:
    new: list[SQLIncident]
    unsolved: list[SQLIncident]
    solved: list[SQLIncident]


# Returns tuple of:
# - list of new incidents
# - list of unsolved incidents
# - list of solved incidents
SolutionDetectionAlgorithm = Callable[[SolutionDetectorContext], SolutionDetectorResult]


def naive_hash(x: SQLIncident) -> int:
    return hash(
        (
            x.violation_name,
            x.ruleset_name,
            x.application_name,
            x.incident_uri,
            x.incident_line,
            json.dumps(x.incident_variables, sort_keys=True),
        )
    )


def solution_detection_naive(ctx: SolutionDetectorContext) -> SolutionDetectorResult:
    result = SolutionDetectorResult([], [], [])

    updating_set: dict[int, SQLIncident] = {naive_hash(x): x for x in ctx.old_incidents}

    for incident in ctx.new_incidents:
        incident_hash = naive_hash(incident)

        if incident_hash in updating_set:
            result.unsolved.append(updating_set.pop(incident_hash))
        else:
            result.new.append(incident)

    result.solved = list(updating_set.values())

    return result


def solution_detection_line_match(
    ctx: SolutionDetectorContext,
) -> SolutionDetectorResult:
    # TODO: Implement line matching solution detection with sequoia-diff or
    # gumtree
    return solution_detection_naive(ctx)


def solution_detection_factory(
    kind: SolutionDetectorKind,
) -> SolutionDetectionAlgorithm:
    match kind:
        case SolutionDetectorKind.NAIVE:
            return solution_detection_naive
        case SolutionDetectorKind.LINE_MATCH:
            return solution_detection_line_match
        case _:
            raise ValueError(f"Unknown solution detection kind: {kind}")
