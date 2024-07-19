import json

from sqlalchemy import bindparam, create_engine, text

from kai.models.kai_config import KaiConfigIncidentStoreSQLiteArgs


def sqlite_engine(args: KaiConfigIncidentStoreSQLiteArgs):
    if args.connection_string:
        return create_engine(args.connection_string)
    else:
        return create_engine(
            f"sqlite://{args.user}:{args.password}@{args.host}:5432/{args.database}",
            client_encoding="utf8",
        )


def sqlite_json_exactly_equal(json_dict: dict):
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
