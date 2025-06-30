from __future__ import annotations

import sys
from datetime import datetime
from difflib import unified_diff
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, computed_field
from sqlalchemy import (
    ARRAY,
    JSON,
    URL,
    Column,
    Connection,
    DateTime,
    Dialect,
    ForeignKey,
    Integer,
    String,
    TypeDecorator,
    event,
    func,
)
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)

# from sqlalchemy.orm import relationship as _relationship
from sqlalchemy.schema import (
    DropConstraint,
    DropTable,
    ForeignKeyConstraint,
    MetaData,
    Table,
)

import kai_mcp_solution_server.analyzer_types as analyzer_types


# https://github.com/pallets-eco/flask-sqlalchemy/issues/722#issuecomment-705672929
def drop_everything(con: Connection) -> None:
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """

    # TODO: Enum data types
    # trans = con.begin()
    inspector = Inspector.from_engine(con.engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables: list[Table] = []
    all_fkeys: list[ForeignKeyConstraint] = []

    for table_name in inspector.get_table_names():
        fkeys: list[ForeignKeyConstraint] = []

        for refl_fkey in inspector.get_foreign_keys(table_name):
            if not refl_fkey["name"]:
                continue

            fkeys.append(ForeignKeyConstraint((), (), name=refl_fkey["name"]))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    # trans.commit()


class SolutionFile(BaseModel):
    uri: str
    content: str


class SolutionChangeSet(BaseModel):
    before: list[SolutionFile]
    after: list[SolutionFile]

    @computed_field
    def diff(self) -> str:
        # use difflib to create a multiline diff

        # if the file names are the same, we assume they are the same file
        # if the file names are different, we create a similarity matrix. If two files have a similarity of 0.8 or more, we assume they are the same file
        # Any files not matched afterwards are considered new/deleted files

        # (before_uri, after_uri) -> (before_file, after_file)
        diff_dict: dict[tuple[str, str], tuple[SolutionFile, SolutionFile]] = {}

        before_files = {f.uri: f for f in self.before}
        after_files = {f.uri: f for f in self.after}

        matched_files = set(before_files.keys()) & set(after_files.keys())
        unmatched_before_files = set(before_files.keys()) - set(after_files.keys())
        unmatched_after_files = set(after_files.keys()) - set(before_files.keys())

        for uri in matched_files:
            before_file = before_files[uri]
            after_file = after_files[uri]
            diff_dict[(before_file.uri, after_file.uri)] = (before_file, after_file)

        # TODO: Implement similarity score
        for uri in unmatched_before_files:
            before_file = before_files[uri]
            diff_dict[(before_file.uri, "")] = (
                before_file,
                SolutionFile(uri="", content=""),
            )

        for uri in unmatched_after_files:
            after_file = after_files[uri]
            diff_dict[("", after_file.uri)] = (
                SolutionFile(uri="", content=""),
                after_file,
            )

        diffs = []
        for (before_uri, after_uri), (before_file, after_file) in diff_dict.items():
            if before_file.content == after_file.content:
                continue

            diff = unified_diff(
                before_file.content.splitlines(keepends=True),
                after_file.content.splitlines(keepends=True),
                fromfile=before_uri,
                tofile=after_uri,
            )

            diffs.append("".join(diff))

        return "\n".join(diffs) if diffs else ""


class SolutionStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MODIFIED = "modified"
    PENDING = "pending"
    UNKNOWN = "unknown"


class SolutionChangeSetJSON(TypeDecorator):  # type: ignore[type-arg]
    """Adapter that bridges Pydantic SolutionChangeSet to Postgres JSON."""

    impl = JSON
    cache_ok = True

    def process_bind_param(
        self, value: SolutionChangeSet | None, dialect: Dialect
    ) -> dict[str, Any] | None:
        if value is None:
            return None
        return value.model_dump(mode="json")

    def process_result_value(
        self, value: Any | None, dialect: Dialect
    ) -> SolutionChangeSet | None:
        if value is None:
            return None
        if isinstance(value, str):
            return SolutionChangeSet.model_validate_json(value)

        return SolutionChangeSet.model_validate(value)


class ListSolutionFileJSON(TypeDecorator):  # type: ignore[type-arg]
    """Adapter that bridges Pydantic list[SolutionFile] to Postgres JSON."""

    impl = JSON
    cache_ok = True

    def process_bind_param(
        self, value: list[SolutionFile] | None, dialect: Dialect
    ) -> list[dict[str, Any]] | None:
        if value is None:
            return None
        return [file.model_dump(mode="json") for file in value]

    def process_result_value(
        self, value: Any | None, dialect: Dialect
    ) -> list[SolutionFile] | None:
        if value is None:
            return None
        if isinstance(value, str):
            return [SolutionFile.model_validate_json(file) for file in value]

        return [SolutionFile.model_validate(file) for file in value]


class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON,
        list[str]: ARRAY(String),
        SolutionChangeSet: SolutionChangeSetJSON,
        list[SolutionFile]: ListSolutionFileJSON,
    }


async def get_async_engine(url: URL | str, drop_all: bool = False) -> AsyncEngine:
    engine = create_async_engine(url)

    async with engine.begin() as conn:
        # NOTE: Only do this in dev/test environments!
        if drop_all:
            print("Dropping all tables", file=sys.stderr)
            await conn.run_sync(drop_everything)

        await conn.run_sync(Base.metadata.create_all)

    return engine


class ViolationID(BaseModel):
    ruleset_name: str
    violation_name: str


violation_hint_association_table = Table(
    "kai_violation_hint_association",
    Base.metadata,
    Column("violation_ruleset_name", String),
    Column("violation_violation_name", String),
    Column(
        "hint_id",
        Integer,
        ForeignKey("kai_hints.id", ondelete="CASCADE", onupdate="CASCADE"),
    ),
    ForeignKeyConstraint(
        ["violation_ruleset_name", "violation_violation_name"],
        ["kai_violations.ruleset_name", "kai_violations.violation_name"],
        ondelete="CASCADE",
        onupdate="CASCADE",
    ),
)


class DBViolation(Base):
    __tablename__ = "kai_violations"

    ruleset_name: Mapped[str] = mapped_column(primary_key=True)
    ruleset_description: Mapped[str | None]

    violation_name: Mapped[str] = mapped_column(primary_key=True)
    violation_category: Mapped[analyzer_types.Category]

    incidents: Mapped[set["DBIncident"]] = relationship(
        back_populates="violation",
        lazy="selectin",
    )
    hints: Mapped[set["DBHint"]] = relationship(
        secondary=violation_hint_association_table,
        back_populates="violations",
        lazy="selectin",
    )

    def __hash__(self) -> int:
        return hash((self.ruleset_name, self.violation_name))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DBViolation):
            raise NotImplementedError(f"Cannot compare DBViolation with {type(other)}")

        return (self.ruleset_name, self.violation_name) == (
            other.ruleset_name,
            other.violation_name,
        )

    def __neq__(self, other: object) -> bool:
        return not self.__eq__(other)


# kai_incidents_solution_association_table = Table(
#     "kai_incidents_solution_association",
#     Base.metadata,
#     Column("incident_id", ForeignKey("kai_incidents.id", primary_key=True, ondelete="CASCADE", onupdate="CASCADE")),
#     Column("solution_id", ForeignKey("kai_solutions.id", primary_key=True, ondelete="CASCADE", onupdate="CASCADE")),
# )


class DBIncident(Base):
    __tablename__ = "kai_incidents"

    __table_args__ = (
        ForeignKeyConstraint(
            ["ruleset_name", "violation_name"],
            ["kai_violations.ruleset_name", "kai_violations.violation_name"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    client_id: Mapped[str]

    uri: Mapped[str]
    message: Mapped[str]
    code_snip: Mapped[str]
    line_number: Mapped[int]
    variables: Mapped[dict[str, Any]]

    # Exclude from __init__
    ruleset_name: Mapped[str] = mapped_column(init=False)
    violation_name: Mapped[str] = mapped_column(init=False)
    violation: Mapped["DBViolation"] = relationship(
        back_populates="incidents",
        lazy="selectin",
    )

    solution_id: Mapped[int | None] = mapped_column(
        ForeignKey("kai_solutions.id", ondelete="SET NULL", onupdate="CASCADE"),
        init=False,
        nullable=True,
    )
    solution: Mapped["DBSolution | None"] = relationship(
        back_populates="incidents",
        uselist=False,
        lazy="selectin",
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DBIncident):
            raise NotImplementedError(f"Cannot compare DBIncident with {type(other)}")

        return self.id == other.id

    def __neq__(self, other: object) -> bool:
        return not self.__eq__(other)


class Solution(BaseModel):
    # TODO: Turn this into a more general "Trajectory" thing?
    change_set: SolutionChangeSet

    reasoning: str | None = None

    solution_status: SolutionStatus

    hint_id: int | None = None


solution_hint_association_table = Table(
    "kai_solution_hint_association",
    Base.metadata,
    Column(
        "solution_id",
        ForeignKey("kai_solutions.id", ondelete="CASCADE", onupdate="CASCADE"),
    ),
    Column(
        "hint_id", ForeignKey("kai_hints.id", ondelete="CASCADE", onupdate="CASCADE")
    ),
)


class DBSolution(Base):
    __tablename__ = "kai_solutions"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    client_id: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        nullable=False,
    )

    change_set: Mapped[SolutionChangeSet]

    # TODO: Make this more robust wrt to change sets and final files.
    final_files: Mapped[list[SolutionFile]]

    reasoning: Mapped[str | None]

    solution_status: Mapped[SolutionStatus]

    def update_solution_status(self) -> None:
        if len(self.final_files) == 0:
            if len(self.change_set.after) == 0:
                self.solution_status = SolutionStatus.ACCEPTED
                return

            self.solution_status = SolutionStatus.PENDING
            return

        after_uris = {file.uri for file in self.change_set.after}
        final_uris = {file.uri for file in self.final_files}

        if len(after_uris) > len(final_uris):
            self.solution_status = SolutionStatus.MODIFIED
            return

        for after_file in self.change_set.after:
            for final_file in self.final_files:
                if after_file.uri != final_file.uri:
                    continue
                if after_file.content != final_file.content:
                    self.solution_status = SolutionStatus.MODIFIED
                    return

        self.solution_status = SolutionStatus.ACCEPTED
        return

    incidents: Mapped[set["DBIncident"]] = relationship(
        back_populates="solution",
        lazy="selectin",
    )

    # TODO: Add whether or not it was RAG or agent?
    # TODO: Store Langgraph output?
    # TODO: Add model information?
    # TODO: Tie into the profile work?

    # TODO: Make this accept more than one hint?
    hints: Mapped[set["DBHint"]] = relationship(
        secondary=solution_hint_association_table,
        back_populates="solutions",
        lazy="selectin",
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DBSolution):
            raise NotImplementedError(f"Cannot compare DBSolution with {type(other)}")

        return self.id == other.id

    def __neq__(self, other: object) -> bool:
        return not self.__eq__(other)


@event.listens_for(DBSolution, "before_insert")
@event.listens_for(DBSolution, "before_update")
def auto_update_solution_status(
    mapper: Any,
    connection: Connection,
    target: DBSolution,
) -> None:
    target.update_solution_status()


class DBHint(Base):
    __tablename__ = "kai_hints"

    # __table_args__ = (
    #     ForeignKeyConstraint(
    #         ["ruleset_name", "violation_name"],
    #         ["kai_violations.ruleset_name", "kai_violations.violation_name"],
    #         ondelete="CASCADE",
    #         onupdate="CASCADE",
    #     ),
    # )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        init=False,
    )

    text: Mapped[str | None]

    # ruleset_name: Mapped[str] = mapped_column()
    # violation_name: Mapped[str] = mapped_column()
    violations: Mapped[set["DBViolation"]] = relationship(
        secondary=violation_hint_association_table,
        back_populates="hints",
        lazy="selectin",
    )

    # Solutions that use this hint
    solutions: Mapped[set["DBSolution"]] = relationship(
        secondary=solution_hint_association_table,
        back_populates="hints",
        lazy="selectin",
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DBHint):
            raise NotImplementedError(f"Cannot compare DBHint with {type(other)}")

        return self.id == other.id

    def __neq__(self, other: object) -> bool:
        return not self.__eq__(other)
