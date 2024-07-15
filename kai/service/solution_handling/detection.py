from dataclasses import dataclass
from typing import Callable, Iterable

from kai.models.kai_config import SolutionDetectorKind
from kai.service.incident_store.sql_types import SQLIncident


@dataclass
class SolutionDetectorContext:
    db_incidents: list[SQLIncident]
    report_incidents: list[SQLIncident]


@dataclass
class SolutionDetectorResult:
    new: Iterable[SQLIncident]
    unsolved: Iterable[SQLIncident]
    solved: Iterable[SQLIncident]


# Returns tuple of:
# - list of new incidents
# - list of unsolved incidents
# - list of solved incidents
SolutionDetectionAlgorithm = Callable[[SolutionDetectorContext], SolutionDetectorResult]


def solution_detection_naive(ctx: SolutionDetectorContext) -> SolutionDetectorResult:
    return SolutionDetectorResult(
        new=list(set(ctx.report_incidents) - set(ctx.db_incidents)),
        unsolved=list(set(ctx.db_incidents).intersection(ctx.report_incidents)),
        solved=list(set(ctx.db_incidents) - set(ctx.report_incidents)),
    )


def solution_detection_line_match(
    ctx: SolutionDetectorContext,
) -> SolutionDetectorResult:
    new_incidents = set(ctx.report_incidents) - set(ctx.db_incidents)
    unsolved_incidents = set(ctx.db_incidents).intersection(ctx.report_incidents)
    solved_incidents = set(ctx.db_incidents) - set(ctx.report_incidents)

    return new_incidents, unsolved_incidents, solved_incidents


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
