import os

from sqlalchemy import and_, create_engine

from kai.kai_logging import initLogging
from kai.model_provider import ModelProvider
from kai.models.kai_config import KaiConfigIncidentStorePostgreSQLArgs
from kai.service.incident_store.incident_store import IncidentStore, SQLIncident, cmd


"""
Responsible for 3 main things:
- Solution storage
- Solution detection
- Solution generation
"""


class PSQLIncidentStore(IncidentStore):
    def __init__(
        self, args: KaiConfigIncidentStorePostgreSQLArgs, model_provider: ModelProvider
    ):
        if args.connection_string:
            self.engine = create_engine(args.connection_string)
        else:
            self.engine = create_engine(
                f"postgresql://{args.user}:{args.password}@{args.host}:5432/{args.database}",
                client_encoding="utf8",
            )

        self.model_provider = model_provider

    def json_exactly_equal(self, json_dict: dict):
        return and_(
            SQLIncident.incident_variables.op("<@")(json_dict),
            SQLIncident.incident_variables.op("@>")(json_dict),
        )


if __name__ == "__main__":
    if os.getenv("LOG_DIR") is not None:
        log_dir = os.getenv("LOG_DIR")
    else:
        log_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../../../logs"
        )

    if os.getenv("LOG_LEVEL") is not None:
        log_level = os.getenv("LOG_LEVEL").upper()
    else:
        log_level = "INFO"

    initLogging(log_level, "DEBUG", log_dir, "kai_psql.log")

    cmd("postgresql")
