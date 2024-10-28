import os
import tomllib
from enum import StrEnum
from typing import Any, Literal, Optional, Self, Union

import yaml
from pydantic import BaseModel, Field, model_validator
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from kai.constants import PATH_KAI

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

    @model_validator(mode="before")
    @classmethod
    def validate_provider(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "provider" not in data:
                data["provider"] = KaiConfigIncidentStoreProvider.POSTGRESQL

        return data

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

    @model_validator(mode="before")
    @classmethod
    def validate_provider(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "provider" not in data:
                data["provider"] = KaiConfigIncidentStoreProvider.SQLITE

        return data

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
    solution_detectors: SolutionDetectorKind = SolutionDetectorKind.LINE_MATCH
    solution_producers: SolutionProducerKind = SolutionProducerKind.TEXT_ONLY

    args: Union[
        KaiConfigIncidentStorePostgreSQLArgs,
        KaiConfigIncidentStoreSQLiteArgs,
    ] = Field(discriminator="provider")


# Model providers


class KaiConfigModels(BaseModel):
    provider: str
    args: dict[str, Any] = Field(default_factory=dict)
    template: Optional[str] = Field(default=None)
    llama_header: Optional[bool] = Field(default=None)
    llm_retries: int = 5
    llm_retry_delay: float = 10.0


# Main config


class TomlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    Helper class to load a TOML file and convert it to a dictionary for
    pydantic-settings.
    """

    def __init__(self, settings_cls: type[BaseSettings], str_path: str):
        self.settings_cls = settings_cls
        self.config = settings_cls.model_config

        self.str_path = str_path

        if not os.path.exists(str_path):
            self.file_content_toml = {}
        else:
            with open(str_path, "r") as f:
                self.file_content_toml = tomllib.loads(f.read())

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        return self.file_content_toml.get(field_name), field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> dict[str, Any]:
        d: dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class KaiConfig(BaseSettings):
    """
    Kai configuration settings. It loads settings from init arguments,
    environment, dotenv, and config files. See
    `KaiConfig.settings_customise_sources` for more details.
    """

    model_config = SettingsConfigDict(env_prefix="KAI__", env_nested_delimiter="__")

    log_level: str | int = "INFO"
    file_log_level: str | int = "INFO"
    log_dir: str = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../logs"
    )
    demo_mode: bool = False
    trace_enabled: bool = False

    # Gunicorn settings
    gunicorn_workers: int = 8
    gunicorn_timeout: int = 3600
    gunicorn_bind: str = "0.0.0.0:8080"

    incident_store: KaiConfigIncidentStore
    models: KaiConfigModels

    solution_consumers: list[SolutionConsumerKind] = Field(
        default_factory=lambda: [SolutionConsumerKind.DIFF_ONLY]
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Config is loaded with the following priority (higher overrides lower):

        - Command line args (not implemented)
        - Config file that is declared on the command line / via init arguments.
        - Environment vars
        - Global config file (kai.config.toml)
        - Default field values
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(
                settings_cls, os.path.join(PATH_KAI, "config.toml")
            ),
        )

    @staticmethod
    def model_validate_filepath(filepath: str) -> "KaiConfig":
        """
        Load a model config from a file and validate it.

        Supported file formats:
        - TOML
        - YAML
        """
        model_dict: dict[str, Any]

        _, file_ext = os.path.splitext(filepath)

        if file_ext == ".toml":
            model_dict = tomllib.load(open(filepath, "rb"))
        elif file_ext == ".yaml" or file_ext == ".yml":
            model_dict = yaml.safe_load(open(filepath, "r"))
        else:
            raise ValueError(f"'{filepath}' has unsupported file type: {file_ext}")

        return KaiConfig(**model_dict)
