from enum import Enum
from typing import Literal, Union

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
    template: str = Field(default="")  # TODO: Hack until we get better templating


# Main config


class KaiConfig(BaseModel):
    log_level: str = "info"
    demo_mode: bool = False

    incident_store: KaiConfigIncidentStore = Field(discriminator="provider")
    models: KaiConfigModels
