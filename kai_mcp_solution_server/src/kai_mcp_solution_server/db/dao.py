from __future__ import annotations

import logging
import sys
from datetime import datetime
from typing import Any

logger = logging.getLogger("kai_mcp_solution_server.db")

from sqlalchemy import (
    ARRAY,
    JSON,
    URL,
    Column,
    Connection,
    DateTime,
    ForeignKey,
    Integer,
    String,
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
from kai_mcp_solution_server.db.python_objects import (
    SolutionChangeSet,
    SolutionFile,
    SolutionStatus,
)
from kai_mcp_solution_server.db.type_decorators import (
    ListSolutionFileJSON,
    SolutionChangeSetJSON,
)


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


solution_before_file_association_table = Table(
    "solution_before_file_association",
    Base.metadata,
    Column(
        "solution_id",
        ForeignKey("kai_solutions.id", ondelete="CASCADE", onupdate="CASCADE"),
    ),
    Column(
        "file_id", ForeignKey("kai_files.id", ondelete="CASCADE", onupdate="CASCADE")
    ),
)

solution_after_file_association_table = Table(
    "solution_after_file_association",
    Base.metadata,
    Column(
        "solution_id",
        ForeignKey("kai_solutions.id", ondelete="CASCADE", onupdate="CASCADE"),
    ),
    Column(
        "file_id", ForeignKey("kai_files.id", ondelete="CASCADE", onupdate="CASCADE")
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

    before: Mapped[set["DBFile"]] = relationship(
        secondary=solution_before_file_association_table,
        back_populates="solution_before",
        lazy="selectin",
    )
    after: Mapped[set["DBFile"]] = relationship(
        secondary=solution_after_file_association_table,
        back_populates="solution_after",
        lazy="selectin",
    )

    reasoning: Mapped[str | None]

    solution_status: Mapped[SolutionStatus]

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

    def update_solution_status(self) -> None:
        previous_status = self.solution_status
        for file in self.after:
            if file.status != SolutionStatus.ACCEPTED:
                self.solution_status = file.status
                if previous_status != self.solution_status:
                    logger.info(
                        f"[DB_STATE_CHANGE] Solution {self.id} status auto-updated: {previous_status} -> {self.solution_status} (due to file {file.uri} with status {file.status})"
                    )
                return

        self.solution_status = SolutionStatus.ACCEPTED
        if previous_status != self.solution_status:
            logger.info(
                f"[DB_STATE_CHANGE] Solution {self.id} status auto-updated: {previous_status} -> ACCEPTED (all files accepted)"
            )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DBSolution):
            raise NotImplementedError(f"Cannot compare DBSolution with {type(other)}")

        return self.id == other.id

    def __neq__(self, other: object) -> bool:
        return not self.__eq__(other)


class DBFile(Base):
    __tablename__ = "kai_files"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        init=False,
    )
    uri: Mapped[str]
    client_id: Mapped[str]
    content: Mapped[str]
    status: Mapped[SolutionStatus]

    solution_before: Mapped[set[DBSolution]] = relationship(
        secondary=solution_before_file_association_table,
        back_populates="before",
        lazy="selectin",
    )
    solution_after: Mapped[set[DBSolution]] = relationship(
        secondary=solution_after_file_association_table,
        back_populates="after",
        lazy="selectin",
    )

    def __hash__(self) -> int:
        return hash(self.id)


@event.listens_for(DBFile, "after_insert")
@event.listens_for(DBFile, "after_update")
@event.listens_for(DBFile, "after_delete")
@event.listens_for(DBSolution, "before_insert")
@event.listens_for(DBSolution, "before_update")
def auto_update_solution_status(
    mapper: Any,
    connection: Connection,
    target: DBSolution | DBFile,
) -> None:

    if isinstance(target, DBSolution):
        # print(f"DBSolution target", file=sys.stderr)
        # print(f"  Solution {target.id}", file=sys.stderr)
        # print(f"    Before status: {target.solution_status}", file=sys.stderr)
        target.update_solution_status()
        # print(f"    After status: {target.solution_status}", file=sys.stderr)
        return

    if target.solution_before or target.solution_after:
        # print(f"DBFile target: {target.uri}", file=sys.stderr)
        # If the file is part of a solution, we need to update the solution status
        for solution in target.solution_before.union(target.solution_after):
            # print(f"  Solution {solution.id}", file=sys.stderr)
            # print(f"    Before status: {solution.solution_status}", file=sys.stderr)
            solution.update_solution_status()
            # print(f"    After status: {solution.solution_status}", file=sys.stderr)


class DBHint(Base):
    __tablename__ = "kai_hints"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        init=False,
    )

    text: Mapped[str | None]

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
