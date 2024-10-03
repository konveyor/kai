import logging
import sys
from pathlib import Path
from typing import Optional, cast

from pydantic import BaseModel

from kai.models.kai_config import KaiConfigModels
from playpen.rpc_server.rpc import (
    DEFAULT_FORMATTER,
    TRACE,
    JsonRpcApplication,
    JsonRpcError,
    JsonRpcErrorCode,
    JsonRpcLoggingHandler,
    JsonRpcRequestResult,
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
    stderrLogLevel: str = "TRACE"
    fileLogLevel: Optional[str] = None
    logDirUri: Optional[str] = None


class KaiRpcApplication(JsonRpcApplication):
    def __init__(self) -> None:
        super().__init__()

        self.initialized = False
        self.config: Optional[KaiRpcApplicationConfig] = None
        self.log = logging.getLogger("kai_rpc_application")


app = KaiRpcApplication()

ERROR_NOT_INITIALIZED = JsonRpcError(
    code=JsonRpcErrorCode.ServerErrorStart,
    message="Server not initialized",
)


@app.add_request(method="shutdown", include_server=True)
def shutdown(app: KaiRpcApplication, server: JsonRpcServer) -> JsonRpcRequestResult:
    server.shutdown_flag = True

    return {}, None


@app.add_request(method="exit", include_server=True)
def exit(app: KaiRpcApplication, server: JsonRpcServer) -> JsonRpcRequestResult:
    server.shutdown_flag = True

    return {}, None


@app.add_request(method="initialize", extract_params=False, include_server=True)
def initialize(
    app: KaiRpcApplication, params: dict, server: JsonRpcServer
) -> JsonRpcRequestResult:
    if app.initialized:
        return {}, JsonRpcError(
            code=JsonRpcErrorCode.ServerErrorStart,
            message="Server already initialized",
        )

    try:
        app.config = KaiRpcApplicationConfig.model_validate(params)

        app.log.setLevel(TRACE)
        app.log.handlers.clear()
        app.log.filters.clear()

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(TRACE)
        stderr_handler.setFormatter(DEFAULT_FORMATTER)
        app.log.addHandler(stderr_handler)

        notify_handler = JsonRpcLoggingHandler(server)
        notify_handler.setLevel(app.config.logLevel)
        notify_handler.setFormatter(DEFAULT_FORMATTER)
        app.log.addHandler(notify_handler)

        if app.config.fileLogLevel and app.config.logDirUri:
            log_dir = Path(app.config.logDirUri)  # FIXME: urlparse?
            log_file = log_dir / "kai_rpc.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(app.config.fileLogLevel)
            file_handler.setFormatter(DEFAULT_FORMATTER)
            app.log.addHandler(file_handler)

        app.log.info(f"Initialized with config: {app.config}")

    except Exception as e:
        return {}, JsonRpcError(
            code=JsonRpcErrorCode.InvalidParams,
            message=str(e),
        )

    app.initialized = True

    return {}, None


@app.add_request(method="setConfig", extract_params=False, include_server=True)
def set_config(
    app: KaiRpcApplication, params: dict, server: JsonRpcServer
) -> JsonRpcRequestResult:
    if not app.initialized:
        return {}, ERROR_NOT_INITIALIZED

    # Basically reset everything
    app.initialized = False
    return cast(JsonRpcRequestResult, initialize(app=app, params=params, server=server))


@app.add_request(method="getRAGSolution")
def get_rag_solution(app: KaiRpcApplication) -> JsonRpcRequestResult:
    if not app.initialized:
        return {}, ERROR_NOT_INITIALIZED

    return {}, None


@app.add_request(method="getCodeplanAgentSolution")
def get_codeplan_agent_solution(app: KaiRpcApplication) -> JsonRpcRequestResult:
    if not app.initialized:
        return {}, ERROR_NOT_INITIALIZED

    return {}, None
