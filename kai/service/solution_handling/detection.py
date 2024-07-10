import enum
from typing import Callable

from kai.service.incident_store.incident_store import SQLIncident


class SolutionDetectionKind(enum.Enum):
    NAIVE = "naive"


# Arguments:
# - list of incidents in the database
# - list of incidents to compare against in the report
# Returns tuple of:
# - list of new incidents
# - list of unsolved incidents
# - list of solved incidents
SolutionDetectionAlgorithm = Callable[
    [list[SQLIncident], list[SQLIncident]],
    tuple[list[SQLIncident], list[SQLIncident], list[SQLIncident]],
]


def solution_detection_naive(
    db_incidents: list[SQLIncident], report_incidents: list[SQLIncident]
) -> tuple[list[SQLIncident], list[SQLIncident], list[SQLIncident]]:
    new_incidents = set(report_incidents) - set(db_incidents)
    unsolved_incidents = set(db_incidents).intersection(report_incidents)
    solved_incidents = set(db_incidents) - set(report_incidents)

    return new_incidents, unsolved_incidents, solved_incidents


SOLUTION_DETECTION_ALGORITHMS: dict[
    SolutionDetectionKind, SolutionDetectionAlgorithm
] = {
    SolutionDetectionKind.NAIVE: solution_detection_naive,
}
