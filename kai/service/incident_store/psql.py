import os

from sqlalchemy import and_, create_engine

from kai.models.kai_config import KaiConfigIncidentStorePostgreSQLArgs
from kai.service.incident_store.sql_types import SQLIncident


def psql_engine(args: KaiConfigIncidentStorePostgreSQLArgs):
    if args.connection_string:
        return create_engine(args.connection_string)
    else:
        return create_engine(
            f"postgresql://{args.user}:{args.password}@{args.host}:5432/{args.database}",
            client_encoding="utf8",
        )


def psql_json_exactly_equal(json_dict: dict):
    return and_(
        SQLIncident.incident_variables.op("<@")(json_dict),
        SQLIncident.incident_variables.op("@>")(json_dict),
    )


if __name__ == "__main__":
    from kai.service.incident_store.incident_store import cmd

    cmd("postgresql")
