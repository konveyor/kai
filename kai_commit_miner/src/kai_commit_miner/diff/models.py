from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.db.python_objects import ViolationID


class IncidentDeltaStatus(StrEnum):
    RESOLVED = "resolved"
    NEW = "new"
    UNCHANGED = "unchanged"
    MOVED = "moved"


class IncidentDelta(BaseModel):
    """The diff status of a single incident between two commits."""

    violation_key: ViolationID
    incident_before: ExtendedIncident | None = None
    incident_after: ExtendedIncident | None = None
    status: IncidentDeltaStatus


class ReportDiff(BaseModel):
    """Complete diff between two analysis reports."""

    commit_before: str
    commit_after: str
    resolved: list[IncidentDelta]
    new: list[IncidentDelta]
    unchanged: list[IncidentDelta]
    moved: list[IncidentDelta]
