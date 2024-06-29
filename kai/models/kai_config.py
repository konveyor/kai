import os
import tomllib
from enum import Enum
from typing import Literal, Optional, Union

import yaml
from pydantic import BaseModel, Field

# Incident store providers


class KaiConfigIncidentStoreProvider(Enum):
    POSTGRESQL = "postgresql"
    IN_MEMORY = "in_memory"


class KaiConfigIncidentStorePostgreSQLArgs(BaseModel):
    host: str
    database: str
    user: str
    password: str


class KaiConfigIncidentStorePostgreSQL(BaseModel):
    provider: Literal["postgresql"]
    args: KaiConfigIncidentStorePostgreSQLArgs


class KaiConfigIncidentStoreInMemoryArgs(BaseModel):
    dummy: bool


class KaiConfigIncidentStoreInMemory(BaseModel):
    provider: Literal["in_memory"]
    args: KaiConfigIncidentStoreInMemoryArgs


KaiConfigIncidentStore = Union[
    KaiConfigIncidentStorePostgreSQL,
    KaiConfigIncidentStoreInMemory,
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
