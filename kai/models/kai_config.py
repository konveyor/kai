import os
import tomllib
from enum import StrEnum
from typing import Literal, Optional, Self, Union

import yaml
from pydantic import BaseModel, Field, model_validator

"""
https://docs.pydantic.dev/2.0/migration/#required-optional-and-nullable-fields

State                                               | Field Definition
----------------------------------------------------+---------------------------
Required, cannot be None                            | f1: str
Not required, cannot be None, is 'abc' by default   | f2: str = 'abc'
Required, can be None                               | f3: Optional[str]
Not required, can be None, is None by default       | f4: Optional[str] = None
Not required, can be None, is 'abc' by default      | f5: Optional[str] = 'abc'
Required, can be any type (including None)          | f6: Any
Not required, can be any type (including None)      | f7: Any = None
"""

# Incident store providers


class KaiConfigIncidentStoreProvider(StrEnum):
    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"


class SolutionDetectorKind(StrEnum):
    NAIVE = "naive"
    LINE_MATCH = "line_match"


class SolutionProducerKind(StrEnum):
    TEXT_ONLY = "text_only"
    LLM_LAZY = "llm_lazy"


class SolutionConsumerKind(StrEnum):
    DIFF_ONLY = "diff_only"
    BEFORE_AND_AFTER = "before_and_after"
    LLM_SUMMARY = "llm_summary"


class KaiConfigIncidentStorePostgreSQLArgs(BaseModel):
    provider: Literal[KaiConfigIncidentStoreProvider.POSTGRESQL]

    host: Optional[str] = None
    database: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None

    connection_string: Optional[str] = None

    @model_validator(mode="after")
    def validate_connection_string(self) -> Self:
        connection_string_present = self.connection_string is not None
        parameters_present = (
            (self.host is not None)
            and (self.database is not None)
            and (self.user is not None)
            and (self.password is not None)
        )

        if connection_string_present == parameters_present:
            raise ValueError(
                "Must provide one of connection_string or [host, database, user, password]"
            )

        return self

    solution_detection: SolutionDetectorKind = SolutionDetectorKind.NAIVE


class KaiConfigIncidentStoreSQLiteArgs(BaseModel):
    provider: Literal[KaiConfigIncidentStoreProvider.SQLITE]

    host: Optional[str] = None
    database: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None

    connection_string: Optional[str] = None

    @model_validator(mode="after")
    def validate_connection_string(self) -> Self:
        connection_string_present = self.connection_string is not None
        parameters_present = (
            (self.host is not None)
            and (self.database is not None)
            and (self.user is not None)
            and (self.password is not None)
        )

        if connection_string_present == parameters_present:
            raise ValueError(
                "Must provide one of connection_string or [host, database, user, password]"
            )

        return self

    solution_detection: SolutionDetectorKind = SolutionDetectorKind.NAIVE


KaiConfigIncidentStoreArgs = Union[
    KaiConfigIncidentStorePostgreSQLArgs,
    KaiConfigIncidentStoreSQLiteArgs,
]


class KaiConfigIncidentStore(BaseModel):
    solution_detectors: SolutionDetectorKind
    solution_producers: SolutionProducerKind

    args: Union[
        KaiConfigIncidentStorePostgreSQLArgs,
        KaiConfigIncidentStoreSQLiteArgs,
    ] = Field(discriminator="provider")


# Model providers


class KaiConfigModels(BaseModel):
    provider: str
    args: dict
    template: Optional[str] = Field(default=None)
    llama_header: Optional[bool] = Field(default=None)
    llm_retries: int = 5
    llm_retry_delay: float = 10.0


# Main config


class KaiConfig(BaseModel):
    log_level: str = "info"
    file_log_level: str = "info"
    log_dir: str = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../logs"
    )
    demo_mode: bool = False
    trace_enabled: bool = False

    incident_store: KaiConfigIncidentStore
    models: KaiConfigModels

    solution_consumers: list[SolutionConsumerKind] = Field(
        default_factory=lambda: [SolutionConsumerKind.DIFF_ONLY]
    )

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
