from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.db import dao
from kai_mcp_solution_server.db.python_objects import SolutionFile, SolutionStatus

T = TypeVar("T")


class PaginatedResult(BaseModel, Generic[T]):
    items: list[T]
    total: int
    offset: int
    limit: int


# --- Incident schemas ---


class IncidentSummary(BaseModel):
    id: int
    client_id: str
    uri: str
    message: str
    line_number: int
    ruleset_name: str
    violation_name: str
    solution_id: int | None = None

    @classmethod
    def from_db(cls, i: dao.DBIncident) -> IncidentSummary:
        return cls(
            id=i.id,
            client_id=i.client_id,
            uri=i.uri,
            message=i.message,
            line_number=i.line_number,
            ruleset_name=i.ruleset_name,
            violation_name=i.violation_name,
            solution_id=i.solution_id,
        )


class IncidentDetail(IncidentSummary):
    code_snip: str = ""
    variables: dict[str, Any] = Field(default_factory=dict)


# --- Hint schemas ---


class HintSummary(BaseModel):
    id: int
    text: str | None = None
    created_at: datetime
    violation_count: int = 0
    solution_count: int = 0

    @classmethod
    def from_db(cls, h: dao.DBHint) -> HintSummary:
        return cls(
            id=h.id,
            text=h.text,
            created_at=h.created_at,
            violation_count=len(h.violations),
            solution_count=len(h.solutions),
        )


# --- Violation schemas ---


class ViolationSummary(BaseModel):
    ruleset_name: str
    violation_name: str
    ruleset_description: str | None = None
    violation_category: str
    incident_count: int = 0
    hint_count: int = 0


class ViolationDetail(ViolationSummary):
    incidents: list[IncidentSummary] = []
    hints: list[HintSummary] = []


# --- Solution schemas ---


class SolutionSummary(BaseModel):
    id: int
    client_id: str
    created_at: datetime
    solution_status: SolutionStatus
    incident_count: int = 0
    reasoning: str | None = None


class SolutionDetail(SolutionSummary):
    before: list[SolutionFile] = []
    after: list[SolutionFile] = []
    incidents: list[IncidentSummary] = []
    hints: list[HintSummary] = []


# --- Collection schemas ---


class CollectionCreate(BaseModel):
    name: str
    description: str | None = None
    source_repo: str | None = None
    migration_type: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class CollectionUpdate(BaseModel):
    description: str | None = None
    source_repo: str | None = None
    migration_type: str | None = None
    metadata: dict[str, Any] | None = None


class CollectionSummary(BaseModel):
    id: int
    name: str
    description: str | None = None
    source_repo: str | None = None
    migration_type: str | None = None
    created_at: datetime
    solution_count: int = 0
    incident_count: int = 0


class CollectionDetail(CollectionSummary):
    metadata: dict[str, Any] = Field(default_factory=dict)


# --- Request schemas for tool-mirroring endpoints ---


class CreateIncidentRequest(BaseModel):
    client_id: str
    extended_incident: ExtendedIncident


class CreateMultipleIncidentsRequest(BaseModel):
    client_id: str
    extended_incidents: list[ExtendedIncident]


class CreateSolutionRequest(BaseModel):
    client_id: str
    incident_ids: list[int]
    before: list[SolutionFile]
    after: list[SolutionFile]
    reasoning: str | None = None
    used_hint_ids: list[int] | None = None


class AcceptFileRequest(BaseModel):
    client_id: str
    solution_file: SolutionFile


class RejectFileRequest(BaseModel):
    client_id: str
    file_uri: str


class AddToCollectionRequest(BaseModel):
    solution_ids: list[int] = Field(default_factory=list)
    incident_ids: list[int] = Field(default_factory=list)


# --- Bulk operations ---


class IngestCommitRequest(BaseModel):
    client_id: str
    collection_id: int | None = None
    incidents: list[ExtendedIncident]
    before_files: list[SolutionFile]
    after_files: list[SolutionFile]
    reasoning: str | None = None


class IngestCommitResponse(BaseModel):
    incident_ids: list[int]
    solution_id: int
    collection_id: int | None = None
