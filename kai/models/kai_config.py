from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel, Field, field_validator, root_validator


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
    todo: bool


class KaiConfigIncidentStoreInMemory(BaseModel):
    provider: Literal["in_memory"]
    args: KaiConfigIncidentStoreInMemoryArgs


KaiConfigIncidentStore = Union[
    KaiConfigIncidentStorePostgreSQL,
    KaiConfigIncidentStoreInMemory,
]


class KaiConfigModels(BaseModel):
    provider: str
    args: dict


class KaiConfig(BaseModel):
    log_level: str = "info"
    demo_mode: bool = False

    incident_store: KaiConfigIncidentStore = Field(discriminator="provider")
    models: KaiConfigModels
