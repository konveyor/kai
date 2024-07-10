from sqlalchemy import bindparam, create_engine, text

from kai.model_provider import ModelProvider
from kai.models.kai_config import KaiConfigIncidentStoreSQLiteArgs
from kai.service.incident_store.incident_store import IncidentStore


class SQLiteIncidentStore(IncidentStore):
    def __init__(
        self, args: KaiConfigIncidentStoreSQLiteArgs, model_provider: ModelProvider
    ):
        if args.connection_string:
            self.engine = create_engine(args.connection_string)
        else:
            self.engine = create_engine(
                f"sqlite://{args.user}:{args.password}@{args.host}:5432/{args.database}",
                client_encoding="utf8",
            )

        self.model_provider = model_provider

    def json_exactly_equal(self, json_dict: dict):
        return text(
            """
        (
            SELECT key, value
            FROM json_tree(SQLIncident.incident_variables)
            WHERE type != 'object'
            ORDER BY key, value
        ) = (
            SELECT key, value
            FROM json_tree(:json_dict)
            WHERE type != 'object'
            ORDER BY key, value
        )
        """
        ).bindparams(bindparam("json_dict", json_dict))
