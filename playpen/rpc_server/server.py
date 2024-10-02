import logging
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

    logLevel: str = "INFO"
    fileLogLevel: Optional[str] = None
    logDirUri: Optional[str] = None


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
def shutdown(app: KaiRpcApplication, server: JsonRpcServer):
    server.shutdown_flag = True

    return {}, None


@app.add_request(method="exit", include_server=True)
def exit(app: KaiRpcApplication, server: JsonRpcServer):
    server.shutdown_flag = True

    return {}, None


@app.add_request(method="initialize", extract_params=False, include_server=True)
def initialize(app: KaiRpcApplication, params: dict, server: JsonRpcServer):
    if app.initialized:
        return {}, JsonRpcError(
            code=JsonRpcErrorCode.ServerErrorStart,
            message="Server already initialized",
        )

    try:
        app.config = KaiRpcApplicationConfig.model_validate(params)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        root_logger.handlers.clear()

        notify_handler = JsonRpcLoggingHandler(server)
        notify_handler.setLevel(app.config.logLevel)
        root_logger.addHandler(notify_handler)

        if app.config.fileLogLevel and app.config.logDirUri:
            log_dir = Path(app.config.logDirUri)  # FIXME: urlparse?
            log_file = log_dir / "kai_rpc.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(app.config.fileLogLevel)

            root_logger.addHandler(file_handler)

        log.info(f"Initialized with config: {app.config}")

    except Exception as e:
        return {}, JsonRpcError(
            code=JsonRpcErrorCode.InvalidParams,
            message=str(e),
        )

    app.initialized = True

    return {}, None


@app.add_request(method="setConfig", extract_params=False, include_server=True)
def set_config(app: KaiRpcApplication, params: dict, server: JsonRpcServer):
    if not app.initialized:
        return {}, ERROR_NOT_INITIALIZED

    # Basically reset everything
    app.initialized = False
    return initialize(app=app, params=params, server=server)


@app.add_request(method="getRAGSolution")
def get_rag_solution(app: KaiRpcApplication):
    if not app.initialized:
        return {}, ERROR_NOT_INITIALIZED

    return {}, None


@app.add_request(method="getCodeplanAgentSolution")
def get_codeplan_agent_solution(app: KaiRpcApplication):
    if not app.initialized:
        return {}, ERROR_NOT_INITIALIZED

    return {}, None
