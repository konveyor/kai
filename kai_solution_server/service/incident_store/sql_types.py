import datetime
from enum import Enum
from typing import Any, Optional, Type

from sqlalchemy import (
    VARCHAR,
    Column,
    DateTime,
    Dialect,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    TypeDecorator,
    func,
)
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from kai import analyzer_types as report_types
from kai_solution_server.service.solution_handling.solution_types import Solution


class SQLSolutionType(TypeDecorator):  # type: ignore[type-arg]
    impl = VARCHAR
    cache_ok = False

    def process_bind_param(
        self, value: Optional[Solution], dialect: Dialect
    ) -> str | None:
        # Into the db
        if value is None:
            return None

        return value.model_dump_json()

    def process_result_value(
        self, value: str | None, dialect: Dialect
    ) -> Solution | None:
        # Out of the db
        if value is None:
            return None

        return Solution.model_validate_json(value)


def SQLEnum(enum_type: Type[Enum]) -> Enum:
    """
    The default behavior of the Enum type in SQLAlchemy is to store the enum's name,
    but we want to store the enum's value. This class is a workaround for that.
    """

    return Enum(
        value=enum_type.__name__,
        names=[(e.value, e.value) for e in enum_type],
    )


SQLCategory: Enum = SQLEnum(report_types.Category)


# ignoring types while waiting for: https://github.com/sqlalchemy/sqlalchemy/issues/6810
class SQLBase(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON()
        .with_variant(postgresql.JSONB(), "postgresql") # type: ignore
        .with_variant(sqlite.JSON(), "sqlite"),
        list[str]: JSON()
        .with_variant(postgresql.JSONB(), "postgresql") #type: ignore
        .with_variant(sqlite.JSON(), "sqlite"),
        Solution: SQLSolutionType,
    }


class SQLUnmodifiedReport(SQLBase):
    __tablename__ = "unmodified_reports"

    application_name: Mapped[str] = mapped_column(primary_key=True)
    report_id: Mapped[str] = mapped_column(primary_key=True)

    generated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), server_default=func.now()
    )
    report: Mapped[dict[str, Any]]


class SQLApplication(SQLBase):
    __tablename__ = "applications"

    application_name: Mapped[str] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(primary_key=True)
    repo_uri_origin: Mapped[str]
    repo_uri_local: Mapped[str]
    current_branch: Mapped[str]
    current_commit: Mapped[str]
    generated_at: Mapped[datetime.datetime]

    incidents: Mapped[list["SQLIncident"]] = relationship(
        back_populates="application", cascade="all, delete-orphan"
    )


class SQLRuleset(SQLBase):
    __tablename__ = "rulesets"

    ruleset_name: Mapped[str] = mapped_column(primary_key=True)

    tags: Mapped[list[str]]

    violations: Mapped[list["SQLViolation"]] = relationship(
        back_populates="ruleset", cascade="all, delete-orphan"
    )


class SQLViolation(SQLBase):
    __tablename__ = "violations"

    violation_name: Mapped[str] = mapped_column(primary_key=True)
    ruleset_name: Mapped[int] = mapped_column(
        ForeignKey("rulesets.ruleset_name"), primary_key=True
    )

    category: Mapped[SQLCategory]  # type: ignore
    labels: Mapped[list[str]]

    ruleset: Mapped[SQLRuleset] = relationship(back_populates="violations")
    incidents: Mapped[list["SQLIncident"]] = relationship(
        back_populates="violation", cascade="all, delete-orphan"
    )


class SQLAcceptedSolution(SQLBase):
    __tablename__ = "accepted_solutions"

    solution_id: Mapped[int] = mapped_column(primary_key=True)
    solution: Mapped[Solution]

    incidents: Mapped[list["SQLIncident"]] = relationship(
        back_populates="solution", cascade="all, delete-orphan"
    )


class SQLIncident(SQLBase):
    __tablename__ = "incidents"

    incident_id: Mapped[int] = mapped_column(primary_key=True)

    violation_name = Column(String)
    ruleset_name = Column(String)
    application_name: Mapped[str] = mapped_column(String)
    application_path: Mapped[str] = mapped_column(String)
    incident_uri: Mapped[str]
    incident_message: Mapped[str]
    incident_snip: Mapped[str]
    incident_line: Mapped[int]  # 0-indexed!
    incident_variables: Mapped[dict[str, Any]]
    solution_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("accepted_solutions.solution_id")
    )

    __table_args__: tuple = (  # type: ignore[type-arg]
        ForeignKeyConstraint(
            [violation_name, ruleset_name],
            [SQLViolation.violation_name, SQLViolation.ruleset_name],
        ),
        ForeignKeyConstraint(
            [application_name, application_path],
            [SQLApplication.application_name, SQLApplication.path],
        ),
        {},
    )

    violation: Mapped[SQLViolation] = relationship(back_populates="incidents")
    application: Mapped[SQLApplication] = relationship(back_populates="incidents")
    solution: Mapped[SQLAcceptedSolution] = relationship(back_populates="incidents")

    def __repr__(self) -> str:
        return f"SQLIncident(violation_name={self.violation_name}, ruleset_name={self.ruleset_name}, application_name={self.application_name}, incident_uri={self.incident_uri}, incident_snip={self.incident_snip:.10}, incident_line={self.incident_line}, incident_variables={self.incident_variables}, solution_id={self.solution_id})"
