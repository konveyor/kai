from __future__ import annotations

import logging as core_logging
import sys
from typing import TYPE_CHECKING

import kai.logging.kai_logging as logging

if TYPE_CHECKING:
    from kai.jsonrpc.core import JsonRpcServer

log = logging.get_logger("jsonrpc")


class JsonRpcLoggingHandler(core_logging.Handler):
    def __init__(self, server: JsonRpcServer, method: str = "logMessage"):
        core_logging.Handler.__init__(self)
        self.server = server
        self.method = method

    def emit(self, record: core_logging.LogRecord) -> None:
        try:
            params = {
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
                "message": record.getMessage(),
            }

            self.server.send_notification(
                method=self.method,
                params=params,
            )
        except Exception:
            print("Failed to log message", file=sys.stderr)
            self.handleError(record)
