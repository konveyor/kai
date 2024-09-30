import functools
import logging
import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, validate_call
from pylsp_jsonrpc.endpoint import Endpoint
from pylsp_jsonrpc.exceptions import JsonRpcInvalidRequest

from kai.models.report_types import ExtendedIncident
from kai.service.kai_application.util import BatchMode
from kai.service.llm_interfacing.model_provider import ModelProvider
from playpen.rpc_server.streams import JsonRpcStreamReader, JsonRpcStreamWriter

log = logging.getLogger(__name__)

_RE_FIRST_CAP = re.compile("(.)([A-Z][a-z]+)")
_RE_ALL_CAP = re.compile("([a-z0-9])([A-Z])")


class KaiRpcLogHandler(logging.Handler):
    def __init__(self, endpoint: Endpoint):
        super().__init__()
        self.endpoint = endpoint

    def emit(self, record):
        try:
            msg = self.format(record)
            self.endpoint.notify(
                "logMessage", {"level": record.levelname, "message": msg}
            )
        except Exception:
            self.handleError(record)


class KaiRpcServerConfig(BaseModel):
    processId: Optional[int]

    rootUri: str
    kantraUri: str
    modelProvider: ModelProvider
    kaiBackendUrl: str

    logLevel: Optional[str] = None
    fileLogLevel: Optional[str] = None
    logDirUri: Optional[Path] = None


class KaiRpcServer:
    def __init__(
        self,
        reader: JsonRpcStreamReader,
        writer: JsonRpcStreamWriter,
        check_parent_process=False,
    ) -> None:
        self._jsonrpc_stream_reader = reader
        self._jsonrpc_stream_writer = writer
        self._check_parent_process = check_parent_process
        self._endpoint = Endpoint(
            self,
            self._jsonrpc_stream_writer.write,
            max_workers=1,
        )

        self._shutdown = False
        self.initialized = False
        self.config = KaiRpcServerConfig.model_construct()

    def start(self) -> None:
        self._jsonrpc_stream_reader.listen(self._endpoint.consume)

    # def consume(self, message) -> None:
    #     self._endpoint.consume(message)

    def __getitem__(self, item):
        if self._shutdown and item != "exit":
            log.debug(f"Ignoring non-exit method during shutdown: {item}")
            item = "invalid_request_after_shutdown"

        method_name = item.replace("/", "__").replace("$", "")
        method_name = _RE_FIRST_CAP.sub(r"\1_\2", method_name)
        method_name = _RE_ALL_CAP.sub(r"\1_\2", method_name).lower()
        method_name = f"m_{method_name}"

        if hasattr(self, method_name):
            method = getattr(self, method_name)

            @functools.wraps(method)
            def handler(params):
                return method(**(params or {}))

            return handler

        raise KeyError()

    def m_shutdown(self):
        self._shutdown = True

    def m_invalid_request_after_shutdown(self):
        return {
            "error": JsonRpcInvalidRequest(
                "Requests after shutdown are not valid"
            ).to_dict(),
        }

    def m_exit(self):
        self._endpoint.shutdown()
        self._jsonrpc_stream_reader.close()
        self._jsonrpc_stream_writer.close()

    def m_initialize(
        self,
        **kwargs,
    ):
        if self.initialized:
            return {
                "error": JsonRpcInvalidRequest(
                    "Server has already been initialized"
                ).to_dict(),
            }

        try:
            self.config = KaiRpcServerConfig(**kwargs)

            logging.root.handlers.clear()

            notify_handler = KaiRpcLogHandler(self._endpoint)
            notify_handler.setLevel(self.config.logLevel or "INFO")

            logging.root.addHandler(notify_handler)

            if self.config.fileLogLevel and self.config.logDirUri:
                log_dir = Path(urlparse(self.config.logDirUri).path)
                log_file = log_dir / "kai_rpc.log"
                log_file.parent.mkdir(parents=True, exist_ok=True)

                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(self.config.fileLogLevel)

                logging.root.addHandler(file_handler)

            log.info(f"Initialized with config: {self.config}")

        except Exception as e:
            msg = f"Failed to parse initialize message: {e}"
            log.exception(msg)
            return {
                "error": JsonRpcInvalidRequest(msg).to_dict(),
            }

        self.initialized = True

        return {}

    def require_initialized(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self.initialized:
                return {
                    "error": JsonRpcInvalidRequest(
                        "Server has not been initialized"
                    ).to_dict(),
                }
            return func(*args, **kwargs)

        return wrapper

    @require_initialized
    def m_set_config(self, **kwargs):
        # Basically just reset everything
        self.initialized = False

        return self.m_initialize(**self.config.model_dump().update(kwargs))

    @validate_call
    def m_get_rag_solution(
        self,
        fileUri: str,
        fileContents: str,
        applicationName: str,
        incidents: list[ExtendedIncident],
        matchMode: BatchMode = BatchMode.SINGLE_GROUP,
        includeSolvedIncidents: bool = True,
        includeLLMResults: bool = False,
        modelProvider: Optional[ModelProvider] = None,
    ):
        return {
            "error": JsonRpcInvalidRequest("Not implemented").to_dict(),
        }

    @validate_call
    def m_get_codeplan_agent_solution_request(
        self,
        fileUri: str,
        fileContents: str,
        applicationName: str,
        incident: ExtendedIncident,
        modelProvider: Optional[ModelProvider] = None,
    ):
        return {
            "error": JsonRpcInvalidRequest("Not implemented").to_dict(),
        }
