import json
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import (
    ColumnElement,
    Engine,
    TextClause,
    and_,
    bindparam,
    create_engine,
    text,
)

from kai.kai_config import (
    KaiConfigIncidentStoreArgs,
    KaiConfigIncidentStorePostgreSQLArgs,
    KaiConfigIncidentStoreProvider,
    KaiConfigIncidentStoreSQLiteArgs,
)
from kai_solution_server.service.incident_store.sql_types import SQLIncident


class IncidentStoreBackend(ABC):
    @abstractmethod
    def create_engine(self) -> Engine:
        pass

    # FIXME(JonahSussman): Narrow this type down
    @abstractmethod
    def json_exactly_equal(self, json_dict: dict[str, Any]) -> Any:
        pass


class PSQLBackend(IncidentStoreBackend):
    def __init__(self, args: KaiConfigIncidentStorePostgreSQLArgs):
        self.args = args

    def create_engine(self) -> Engine:
        if self.args.connection_string:
            return create_engine(self.args.connection_string)
        else:
            return create_engine(
                f"postgresql://{self.args.user}:{self.args.password}@{self.args.host}:5432/{self.args.database}",
                client_encoding="utf8",
            )

    def json_exactly_equal(self, json_dict: dict[str, Any]) -> ColumnElement[bool]:
        return and_(
            SQLIncident.incident_variables.op("<@")(json_dict),
            SQLIncident.incident_variables.op("@>")(json_dict),
        )


class SQLiteBackend(IncidentStoreBackend):
    def __init__(self, args: KaiConfigIncidentStoreSQLiteArgs):
        self.args = args

    def create_engine(self) -> Engine:
        if self.args.connection_string:
            return create_engine(self.args.connection_string)
        else:
            return create_engine(
                f"sqlite://{self.args.user}:{self.args.password}@{self.args.host}:5432/{self.args.database}",
                client_encoding="utf8",
            )

    def json_exactly_equal(self, json_dict: dict[str, Any]) -> TextClause:
        return text(
            """
        (
            SELECT key, value
            FROM json_tree(incidents.incident_variables)
            WHERE type != 'object'
            ORDER BY key, value
        ) = (
            SELECT key, value
            FROM json_tree(json(:json_dict))
            WHERE type != 'object'
            ORDER BY key, value
        )
        """
        ).bindparams(bindparam("json_dict", json.dumps(json_dict)))


def incident_store_backend_factory(
    args: KaiConfigIncidentStoreArgs,
) -> IncidentStoreBackend:
    match args.provider:
        case KaiConfigIncidentStoreProvider.POSTGRESQL:
            return PSQLBackend(args)
        case KaiConfigIncidentStoreProvider.SQLITE:
            return SQLiteBackend(args)
        case _:
            raise ValueError(f"Unknown incident store provider: {args.provider}")
