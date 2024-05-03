from enum import Enum

from pydantic import BaseModel, root_validator


class KaiConfigIncidentStoreArgsPostgreSQL(BaseModel):
    host: str
    database: str
    user: str
    password: str


class KaiConfigIncidentStoreProvider(Enum):
    POSTGRESQL = "postgresql"
    IN_MEMORY = "in_memory"


class KaiConfigIncidentStore(BaseModel):
    provider: str
    args: dict

    @root_validator(pre=True)
    def check_provider(cls, values):
        provider = values.get("provider")
        args_data = values.get("args")

        match provider:
            case KaiConfigIncidentStoreProvider.POSTGRESQL:
                ArgsModel = KaiConfigIncidentStoreArgsPostgreSQL
            # case KaiConfigIncidentStoreProvider.IN_MEMORY:
            #     ArgsModel = KaiConfigIncidentStoreArgsInMemory
            case _:
                raise ValueError(f"Unsupported provider: {provider}")

        values["args"] = ArgsModel(**args_data)

        return values


class KaiConfigModels(BaseModel):
    provider: str
    args: dict


class KaiConfig(BaseModel):
    log_level: str = "info"
    demo_mode: bool = False

    incident_store: KaiConfigIncidentStore
    models: KaiConfigModels
