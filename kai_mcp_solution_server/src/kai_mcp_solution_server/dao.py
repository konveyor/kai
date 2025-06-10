from __future__ import annotations

import sys
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel
from sqlalchemy import (
    ARRAY,
    JSON,
    Column,
    Connection,
    DateTime,
    Dialect,
    ForeignKey,
    Integer,
    String,
    TypeDecorator,
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

# def relationship(*args: Any, **kwargs: Any) -> Any:
#     """A wrapper around sqlalchemy.orm.relationship to set lazy='selectin' by default."""
#     kwargs.setdefault("lazy", "selectin")
#     return _relationship(*args, **kwargs)


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


"""
class PydanticJson(TypeDecorator):
    impl = JSON
    cache_ok = True

    def __init__(self, model: type[BaseModel]) -> None:
        super().__init__(none_as_null=True)
        self.model = model

    def _make_bind_processor(self, string_process, json_serializer):
        if string_process:

            def process(value):
                if value is self.NULL:
                    value = None
                elif isinstance(value, elements.Null) or (
                    value is None and self.none_as_null
                ):
                    return None
                serialized = json_serializer(value)
                return string_process(serialized)

        else:

            def process(value):
                if value is self.NULL:
                    value = None
                elif isinstance(value, elements.Null) or (
                    value is None and self.none_as_null
                ):
                    return None
                return json_serializer(value)

        return process

    def bind_processor(self, dialect):
        string_process = self._str_impl.bind_processor(dialect)
        json_serializer = TypeAdapter(self.model).dump_json
        return self._make_bind_processor(string_process, json_serializer)

    def result_processor(self, dialect, coltype):
        string_process = self._str_impl.result_processor(dialect, coltype)
        json_deserializer = TypeAdapter(self.model).validate_json

        def process(value):
            if value is None:
                return None
            if string_process:
                value = string_process(value)
            return json_deserializer(value)

        return process
"""


class SolutionFile(BaseModel):
    uri: str
    content: str


class SolutionChangeSet(BaseModel):
    diff: str

    before: list[SolutionFile]
    after: list[SolutionFile]


class SolutionStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MODIFIED = "modified"
    PENDING = "pending"
    UNKNOWN = "unknown"


class SolutionChangeSetJSON(TypeDecorator):  # type: ignore[type-arg]
    """Adapter that bridges Pydantic SolutionChangeSet to Postgres JSONB."""

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


class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON,
        list[str]: ARRAY(String),
        SolutionChangeSet: SolutionChangeSetJSON,
    }


async def get_async_engine(url: str, drop_all: bool = False) -> AsyncEngine:
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
    hint_id: Mapped[int | None] = mapped_column(
        ForeignKey("kai_hints.id", ondelete="SET NULL", onupdate="CASCADE"),
        init=False,
        nullable=True,
    )
    hint: Mapped["DBHint | None"] = relationship(
        back_populates="solutions",
        uselist=False,
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
        back_populates="hint",
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
