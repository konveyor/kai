import sys
from enum import StrEnum
from functools import cache
from typing import Any

from pydantic import BaseModel, Field, TypeAdapter
from sqlalchemy import JSON, Engine
from sqlalchemy import Enum as SAEnum
from sqlalchemy import (
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    Text,
    TypeDecorator,
    create_engine,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy.sql import elements

import kai_mcp_solution_server.analyzer_types as analyzer_types

# from difflib import context_diff


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


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSONB}


async def get_async_engine(url: str, drop_all: bool = True) -> AsyncEngine:
    engine = create_async_engine(url)

    async with engine.begin() as conn:
        if drop_all:  # TODO: DONT DO THIS
            print("Dropping all tables", file=sys.stderr)
            await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)

    return engine


class DBViolation(Base):
    __tablename__ = "kai_violations"

    ruleset_name: Mapped[str] = mapped_column(primary_key=True)
    ruleset_description: Mapped[str | None]

    violation_name: Mapped[str] = mapped_column(primary_key=True)
    violation_category: Mapped[analyzer_types.Category]

    incidents: Mapped[list["DBIncident"]] = relationship(back_populates="violation")


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
            # ondelete="CASCADE",
        ),
    )

    violation: Mapped["DBViolation"] = relationship(back_populates="incidents")

    fixes: Mapped[list["DBFix"]] = relationship(back_populates="incident")


class FixStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MODIFIED = "modified"
    UNKNOWN = "unknown"


class DBFix(Base):
    __tablename__ = "kai_fixes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    before_filename: Mapped[str]
    before_text: Mapped[str]

    after_filename: Mapped[str]
    after_text: Mapped[str]

    solution_status: Mapped[FixStatus]

    incident_id: Mapped[int] = mapped_column(
        ForeignKey("kai_incidents.id", ondelete="CASCADE"),
    )
    incident: Mapped["DBIncident"] = relationship(back_populates="fixes")


class DBHint(Base):
    __tablename__ = "kai_hints"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
