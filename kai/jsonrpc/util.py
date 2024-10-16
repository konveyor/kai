import logging
import sys
from typing import Any

from pydantic import AliasChoices, AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

TRACE = logging.DEBUG - 5
DEFAULT_FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def get_logger(
    name: str,
    stderr_level: int | str = "TRACE",
    formatter: logging.Formatter = DEFAULT_FORMATTER,
) -> logging.Logger:
    logging.addLevelName(logging.DEBUG - 5, "TRACE")

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(TRACE)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(stderr_level)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    return logger


def log_record_to_dict(record: logging.LogRecord) -> dict[str, Any]:
    return {
        "name": record.name,
        "levelno": record.levelno,
        "levelname": record.levelname,
        "pathname": record.pathname,
        "filename": record.filename,
        "module": record.module,
        "lineno": record.lineno,
        "funcName": record.funcName,
        "created": record.created,
        "asctime": record.asctime,
        "msecs": record.msecs,
        "relativeCreated": record.relativeCreated,
        "thread": record.thread,
        "threadName": record.threadName,
        "process": record.process,
        "msg": record.msg,
        "args": record.args,
        "message": record.getMessage(),
    }


class CamelCaseBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasChoices(
                field_name,
                to_camel(field_name),
            ),
            serialization_alias=to_camel,
        ),
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return super().model_dump(by_alias=True, **kwargs)
