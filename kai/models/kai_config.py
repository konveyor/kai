import os
import tomllib
from enum import Enum
from typing import Literal, Optional, Union

import yaml
from pydantic import BaseModel, Field, validator

# Incident store providers


class KaiConfigIncidentStoreProvider(Enum):
    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"


class KaiConfigIncidentStorePostgreSQLArgs(BaseModel):
    host: Optional[str] = None
    database: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None

    connection_string: Optional[str] = None

    @validator("connection_string", always=True)
    def validate_connection_string(cls, v, values):
        connection_string_present = v is not None
        parameters_present = all(
            values.get(key) is not None
            for key in ["host", "database", "user", "password"]
        )

        if connection_string_present == parameters_present:
            raise ValueError(
                "Must provide one of connection_string or [host, database, user, password]"
            )

        return v


class KaiConfigIncidentStorePostgreSQL(BaseModel):
    provider: Literal["postgresql"]
    args: KaiConfigIncidentStorePostgreSQLArgs


class KaiConfigIncidentStoreSQLiteArgs(BaseModel):
    host: Optional[str] = None
    database: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None

    connection_string: Optional[str] = None

    @validator("connection_string", always=True)
    def validate_connection_string(cls, v, values):
        connection_string_present = v is not None
        parameters_present = all(
            values.get(key) is not None
            for key in ["host", "database", "user", "password"]
        )

        if connection_string_present == parameters_present:
            raise ValueError(
                "Must provide one of connection_string or [host, database, user, password]"
            )

        return v


class KaiConfigIncidentStoreSQLIte(BaseModel):
    provider: Literal["sqlite"]
    args: KaiConfigIncidentStoreSQLiteArgs


KaiConfigIncidentStore = Union[
    KaiConfigIncidentStorePostgreSQL,
    KaiConfigIncidentStoreSQLIte,
]

# Model providers


class KaiConfigModels(BaseModel):
    provider: str
    args: dict
    template: Optional[str] = Field(default=None)
    llama_header: Optional[bool] = Field(default=None)


# Main config


class KaiConfig(BaseModel):
    log_level: str = "info"
    file_log_level: str = "info"
    log_dir: str = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../logs"
    )
    demo_mode: bool = False
    trace_enabled: bool = False

    incident_store: KaiConfigIncidentStore = Field(discriminator="provider")
    models: KaiConfigModels

    @staticmethod
    def model_validate_filepath(filepath: str):
        """
        Load a model config from a file and validate it.

        Supported file formats:
        - TOML
        - YAML
        """
        model_dict: dict

        _, file_ext = os.path.splitext(filepath)

        if file_ext == ".toml":
            model_dict = tomllib.load(open(filepath, "rb"))
        elif file_ext == ".yaml" or file_ext == ".yml":
            model_dict = yaml.safe_load(open(filepath, "r"))
        else:
            raise ValueError(f"'{filepath}' has unsupported file type: {file_ext}")

        return KaiConfig.model_validate(model_dict)
