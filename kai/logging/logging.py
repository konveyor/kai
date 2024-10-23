import logging
import os
from typing import Self, override

from kai.kai_config import KaiConfig

TRACE = logging.DEBUG - 5


class KaiLogger(logging.Logger):
    configLogLevel: int

    def __init__(self, name: str, configLogLevel: int) -> None:
        super().__init__(name, configLogLevel)
        self.configLogLevel = configLogLevel

    @override
    def getChild(self, suffix: str) -> Self:
        log = super().getChild(suffix)
        log.configLogLevel = self.configLogLevel
        log.setLevel(self.configLogLevel)
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
        # Default to debug, can be overriden at start or program by setting kai_logger
        log = KaiLogger("kai", logging.DEBUG)
        log.configLogLevel = logging.DEBUG

    return log.getChild(childName)


# console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(levelname)s - %(asctime)s - %(name)s - [%(filename)20s:%(lineno)-4s - %(funcName)20s()] - %(message)s"
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
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def setup_file_handler(
    logger: KaiLogger,
    log_file_name: str,
    log_dir: str,
    log_level: str | int = "DEBUG",
    silent: bool = False,
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
    if not silent:
        print(
            f"File logging for '{logger.name}' is set to level '{log_level}' writing to file: '{log_file_path}'"
        )


def init_logging(
    console_log_level: str | int,
    file_log_level: str | int,
    log_dir: str,
    log_file: str = "kai_server.log",
) -> None:
    global log
    log = KaiLogger("kai", logging.DEBUG)
    log.configLogLevel = logging.DEBUG

    setup_console_handler(log, console_log_level)
    setup_file_handler(log, log_file, log_dir, file_log_level)


def init_logging_from_config(config: KaiConfig) -> None:
    log_level: str | int = 0
    if isinstance(config.log_level, str):
        log_level = config.log_level.upper()
    elif isinstance(config.log_level, int):
        log_level = config.log_level
    else:
        # TODO: raise exception
        log_level = logging.DEBUG

    file_log_level: str | int = 0
    if isinstance(config.file_log_level, str):
        file_log_level = config.file_log_level.upper()
    elif isinstance(config.file_log_level, int):
        file_log_level = config.file_log_level
    else:
        # TODO: raise exception
        file_log_level = logging.DEBUG

    init_logging(log_level, file_log_level, config.log_dir)
