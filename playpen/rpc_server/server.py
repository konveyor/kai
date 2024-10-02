import logging
import sys
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from kai.models.kai_config import KaiConfigModels
from playpen.rpc_server.rpc import (
    JsonRpcApplication,
    JsonRpcError,
    JsonRpcErrorCode,
    JsonRpcLoggingHandler,
    JsonRpcServer,
)

log = logging.getLogger(__name__)


class KaiRpcApplicationConfig(BaseModel):
    processId: Optional[int]

    rootUri: str
    kantraUri: str
    modelProvider: KaiConfigModels
    kaiBackendUrl: str

    logLevel: Optional[str] = None
    fileLogLevel: Optional[str] = None
    logDirUri: Optional[Path] = None


class KaiRpcApplication(JsonRpcApplication):
    def __init__(self):
        super().__init__()

        self.initialized = False
        self.config: Optional[KaiRpcApplicationConfig] = None


app = KaiRpcApplication()

ERROR_NOT_INITIALIZED = JsonRpcError(
    code=JsonRpcErrorCode.ServerErrorStart,
    message="Server not initialized",
)


@app.add_request(method="shutdown", include_server=True)
def shutdown(self: KaiRpcApplication, server: JsonRpcServer):
    server.shutdown_flag = True

    return {}, None


@app.add_request(method="exit", include_server=True)
def exit(self: KaiRpcApplication, server: JsonRpcServer):
    server.shutdown_flag = True

    return {}, None


@app.add_request(method="initialize", extract_params=False, include_server=True)
def initialize(self: KaiRpcApplication, params: dict, server: JsonRpcServer):
    if self.initialized:
        return {}, JsonRpcError(
            code=JsonRpcErrorCode.ServerErrorStart,
            message="Server already initialized",
        )

    try:
        self.config = KaiRpcApplicationConfig.model_validate(params)

        logging.root.handlers.clear()

        notify_handler = JsonRpcLoggingHandler(server)
        notify_handler.setLevel(self.config.logLevel or logging.INFO)

        logging.root.addHandler(notify_handler)

        if self.config.fileLogLevel and self.config.logDirUri:
            log_dir = self.config.logDirUri
            log_file = log_dir / "kai_rpc.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(self.config.fileLogLevel)

            logging.root.addHandler(file_handler)

        log.info(f"Initialized with config: {self.config}")

    except Exception as e:
        return {}, JsonRpcError(
            code=JsonRpcErrorCode.InvalidParams,
            message=str(e),
        )

    self.initialized = True

    return {}, None


@app.add_request(method="setConfig", extract_params=False, include_server=True)
def set_config(self: KaiRpcApplication, params: dict, server: JsonRpcServer):
    if not self.initialized:
        return {}, ERROR_NOT_INITIALIZED

    # Basically reset everything
    self.initialized = False
    return initialize(app=self, params=params, server=server)


@app.add_request(method="getRAGSolution")
def get_rag_solution(self: KaiRpcApplication):
    if not self.initialized:
        return {}, ERROR_NOT_INITIALIZED

    return {}, None


@app.add_request(method="getCodeplanAgentSolution")
def get_codeplan_agent_solution(self: KaiRpcApplication):
    if not self.initialized:
        return {}, ERROR_NOT_INITIALIZED

    return {}, None
