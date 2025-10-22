import logging
import os
import sys
from pathlib import Path

from kai.jsonrpc.util import AutoAbsPath, AutoUpperStr, CamelCaseBaseModel

TRACE = logging.DEBUG - 5
logging.addLevelName(TRACE, "TRACE")


class KaiLogConfig(CamelCaseBaseModel):
    log_level: AutoUpperStr | int = "INFO"
    stderr_log_level: AutoUpperStr | int = "TRACE"
    file_log_level: AutoUpperStr | int = "DEBUG"
    log_dir_path: AutoAbsPath = Path("./logs")
    log_file_name: str = "kai_server.log"


class KaiLogger(logging.Logger):
    configLogLevel: int

    def __init__(self, name: str, configLogLevel: int, log_level: int):
        super().__init__(name, log_level)
        self.configLogLevel = configLogLevel

    def getChild(self, suffix: str) -> "KaiLogger":
        log = KaiLogger(
            name=".".join([self.name, suffix]),
            configLogLevel=self.configLogLevel,
            log_level=logging.NOTSET,
        )
        log.parent = self
        return log

    def setLevel(self, level: str | int) -> None:
        if isinstance(level, int):
            if level == self.configLogLevel:
                return super().setLevel(level)
            else:
                self.debug("tried to set level not matching config")
                return
        if isinstance(level, str):
            name_mapping = logging.getLevelNamesMapping()
            name_mapping["TRACE"] = TRACE
            if level in name_mapping and name_mapping[level] == self.configLogLevel:
                return super().setLevel(level=self.configLogLevel)
            else:
                self.debug("tried to set level not matching config")
                return


log: KaiLogger | None = None


def get_logger(childName: str) -> KaiLogger:
    global log
    if not log:
        # Default to debug, can be overridden at start or program by setting kai_logger
        log = KaiLogger("kai", logging.NOTSET, logging.NOTSET)

    return log.getChild(childName)


# console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(levelname)s - %(asctime)s - %(name)s - %(threadName)s - [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s"
)


def process_log_dir_replacements(log_dir: str) -> str:
    ##
    # We want to replace $pwd with the location of the Kai project directory,
    # this is needed to help with specifying from configuration
    ##
    if log_dir.startswith("$pwd"):
        current_directory = os.getcwd()
        kai_project_directory = os.path.abspath(current_directory)
        log_dir = log_dir.replace("$pwd", kai_project_directory, 1)
        log_dir = os.path.normpath(log_dir)
    return log_dir


def setup_console_handler(logger: KaiLogger, log_level: str | int = "INFO") -> None:
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def setup_file_handler(
    logger: KaiLogger,
    log_file_name: str,
    log_dir: str,
    log_level: str | int = "DEBUG",
) -> None:
    # Ensure any needed log directories exist
    log_dir = process_log_dir_replacements(log_dir)
    log_file_path = os.path.join(log_dir, log_file_name)
    if log_dir.startswith("$pwd"):
        log_dir = os.path.join(os.getcwd(), log_dir[5:])
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def init_logging(
    log_level: str | int,
    file_log_level: str | int,
    log_dir_path: str | Path,
    log_file_name: str = "kai_server.log",
) -> None:
    if isinstance(log_dir_path, Path):
        log_dir_path = str(log_dir_path)

    global log
    if not log:
        log = KaiLogger("kai", logging.NOTSET, logging.NOTSET)

    for handler in log.handlers:
        log.removeHandler(handler)
    setup_console_handler(log, log_level)
    setup_file_handler(log, log_file_name, log_dir_path, file_log_level)

    if not log:
        raise NotImplementedError()

    for child_log in log.getChildren():
        child_log.handlers = []

    log.info(
        "We have inited the logger: file_logging: %s console_logging: %s",
        file_log_level,
        log_level,
    )


def init_logging_from_log_config(config: KaiLogConfig) -> None:
    init_logging(
        config.log_level,
        config.file_log_level,
        config.log_dir_path,
        config.log_file_name,
    )
