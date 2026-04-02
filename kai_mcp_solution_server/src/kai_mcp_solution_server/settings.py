from typing import Annotated, Any

from pydantic import model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict
from sqlalchemy import URL, make_url


class SolutionServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kai_")

    db_dsn: Annotated[URL, NoDecode]
    """
    Example DSNs:
    - PostgreSQL: `postgresql+asyncpg://username:password@host:port/database`
    - SQLite: `sqlite+aiosqlite:///path/to/database.db`
    """

    llm_params: dict[str, Any] | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_db_dsn(cls, data: Any) -> Any:
        """
        Environment variables added:
        - `KAI_DB_DRIVERNAME`
        - `KAI_DB_USERNAME`
        - `KAI_DB_PASSWORD`
        - `KAI_DB_HOST`
        - `KAI_DB_PORT`
        - `KAI_DB_DATABASE`

        A DSN may be provided as a URL string via the KAI_DB_DSN environment variable, or as
        a JSON object with the above keys. KAI_DB_DSN takes precedence over the other
        environment variables.

        If KAI_DB_DSN is provided as a JSON object with the keys `drivername`, `username`,
        `password`, `host`, `port`, and `database`, it will be converted to a SQLAlchemy URL
        object.

        Example DSNs:
        - PostgreSQL: `postgresql+asyncpg://username:password@host:port/database`
        - SQLite: `sqlite+aiosqlite:///path/to/database.db`
        - MySQL: `mysql+asyncmy://username:password@host:port/database`
        - MariaDB: `mariadb+asyncmy://username:password@host:port/database`

        Example JSON object:
        ```json
        {
            "drivername": "postgresql+asyncpg",
            "username": "kai",
            "password": "dog",
            "host": "localhost",
            "port": 5432,
            "database": "kai"
        }
        ```
        """
        if isinstance(data, dict):
            dsn_value = data.get("db_dsn")
            if isinstance(dsn_value, str):
                try:
                    data["db_dsn"] = make_url(dsn_value)
                except Exception:
                    pass
            elif isinstance(dsn_value, dict):
                kwargs = {}
                if "drivername" in dsn_value:
                    kwargs["drivername"] = dsn_value["drivername"]
                if "username" in dsn_value:
                    kwargs["username"] = dsn_value["username"]
                if "password" in dsn_value:
                    kwargs["password"] = dsn_value["password"]
                if "host" in dsn_value:
                    kwargs["host"] = dsn_value["host"]
                if "port" in dsn_value:
                    kwargs["port"] = dsn_value["port"]
                if "database" in dsn_value:
                    kwargs["database"] = dsn_value["database"]
                data["db_dsn"] = URL.create(**kwargs)

        return data
