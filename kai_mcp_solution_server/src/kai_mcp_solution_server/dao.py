from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from functools import cache
from typing import Any, Optional

from pydantic import BaseModel, Field, TypeAdapter
from sqlalchemy import JSON, Connection, DateTime, Engine
from sqlalchemy import Enum as SAEnum
from sqlalchemy import (
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    Text,
    TypeDecorator,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy.schema import (
    DropConstraint,
    DropTable,
    ForeignKeyConstraint,
    MetaData,
    Table,
)
from sqlalchemy.sql import elements

import kai_mcp_solution_server.analyzer_types as analyzer_types

# from difflib import context_diff


# https://github.com/pallets-eco/flask-sqlalchemy/issues/722#issuecomment-705672929
def drop_everything(con: Connection):
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    # trans = con.begin()
    inspector = Inspector.from_engine(con.engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue

            fkeys.append(ForeignKeyConstraint((), (), name=fkey["name"]))

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


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSONB,
        dict["str", "Any"]: JSONB,
    }


async def get_async_engine(url: str, drop_all: bool = False) -> AsyncEngine:
    engine = create_async_engine(url)

    async with engine.begin() as conn:
        if drop_all:  # TODO: DONT DO THIS
            print("Dropping all tables", file=sys.stderr)
            await conn.run_sync(drop_everything)

        await conn.run_sync(Base.metadata.create_all)

    return engine


class DBViolation(Base):
    __tablename__ = "kai_violations"

    ruleset_name: Mapped[str] = mapped_column(primary_key=True)
    ruleset_description: Mapped[str | None]

    violation_name: Mapped[str] = mapped_column(primary_key=True)
    violation_category: Mapped[analyzer_types.Category]

    incidents: Mapped[set["DBIncident"]] = relationship(back_populates="violation")
    hints: Mapped[set["DBHint"]] = relationship(back_populates="violation")


class DBIncident(Base):
    __tablename__ = "kai_incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    uri: Mapped[str]
    message: Mapped[str]
    code_snip: Mapped[str]
    line_number: Mapped[int]
    variables: Mapped[dict[str, Any]]

    ruleset_name: Mapped[str] = mapped_column()
    violation_name: Mapped[str] = mapped_column()
    __table_args__ = (
        ForeignKeyConstraint(
            ["ruleset_name", "violation_name"],
            ["kai_violations.ruleset_name", "kai_violations.violation_name"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    violation: Mapped["DBViolation"] = relationship(back_populates="incidents")

    solutions: Mapped[set["DBSolution"]] = relationship(back_populates="incident")
    hints: Mapped[set["DBHint"]] = relationship(back_populates="incident")


class SolutionStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MODIFIED = "modified"
    UNKNOWN = "unknown"


class Solution(BaseModel):
    before_uri: str
    before_content: str

    after_uri: str
    after_content: str

    hint_id: int | None = None

    solution_status: SolutionStatus


class DBSolution(Base):
    __tablename__ = "kai_solutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    before_uri: Mapped[str]
    before_content: Mapped[str]

    after_uri: Mapped[str]
    after_content: Mapped[str]

    solution_status: Mapped[SolutionStatus]

    incident_id: Mapped[int] = mapped_column(
        ForeignKey("kai_incidents.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    incident: Mapped["DBIncident"] = relationship(back_populates="solutions")

    hint_id: Mapped[int | None] = mapped_column(
        ForeignKey("kai_hints.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    hint: Mapped["DBHint | None"] = relationship(
        back_populates="solutions",
        foreign_keys=[hint_id],
        uselist=False,
    )


class DBHint(Base):
    __tablename__ = "kai_hints"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    text: Mapped[str | None]

    incident_id: Mapped[int] = mapped_column(
        ForeignKey("kai_incidents.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    incident: Mapped["DBIncident"] = relationship(
        back_populates="hints",
        foreign_keys=[incident_id],
    )

    ruleset_name: Mapped[str] = mapped_column()
    violation_name: Mapped[str] = mapped_column()

    __table_args__ = (
        ForeignKeyConstraint(
            ["ruleset_name", "violation_name"],
            ["kai_violations.ruleset_name", "kai_violations.violation_name"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )

    violation: Mapped["DBViolation"] = relationship(back_populates="hints")

    solutions: Mapped[set["DBSolution"]] = relationship(back_populates="hint")
