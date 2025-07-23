import json
from typing import Any

from sqlalchemy import JSON, Dialect, TypeDecorator

from kai_mcp_solution_server.db.python_objects import SolutionChangeSet, SolutionFile


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
            load = json.loads(value)
            if isinstance(load, dict):
                load = [load]
            elif not isinstance(load, list):
                raise ValueError(f"Expected a list or dict, got {type(load)}: {load}")

            return [SolutionFile.model_validate(file) for file in load]

        return [SolutionFile.model_validate(file) for file in value]
