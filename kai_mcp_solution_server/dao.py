from enum import StrEnum
from functools import cache
from typing import Any

from analyzer_types import ExtendedIncident
from pydantic import BaseModel, Field, TypeAdapter
from sqlalchemy import JSON, Engine
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Integer, Text, TypeDecorator, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.sql import elements

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


async def get_async_engine(url: str) -> AsyncEngine:
    engine = create_async_engine(url)

    async with engine.begin() as conn:
        # TODO: DONT DO THIS
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return engine


class SolutionStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MODIFIED = "modified"
    UNKNOWN = "unknown"


class DBKaiSolution(Base):
    __tablename__ = "kai_solutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    before_filename: Mapped[str] = mapped_column(Text, nullable=False)
    before_text: Mapped[str] = mapped_column(Text, nullable=False)

    after_filename: Mapped[str] = mapped_column(Text, nullable=False)
    after_text: Mapped[str] = mapped_column(Text, nullable=False)

    extended_incident: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    status: Mapped[SolutionStatus] = mapped_column(
        SAEnum(SolutionStatus, name="solution_status", native_enum=False),
        nullable=False,
    )

    hint: Mapped[str] = mapped_column(Text, nullable=True)
