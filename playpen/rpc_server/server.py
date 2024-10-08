import logging
import sys
import traceback
from pathlib import Path
from typing import Optional, cast

import requests
from pydantic import BaseModel

from kai.models.kai_config import KaiConfigModels
from kai.routes.get_incident_solutions_for_file import (
    PostGetIncidentSolutionsForFileParams,
)
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


@app.add_request(method="echo", params_model=dict)
def echo(app: KaiRpcApplication, params: dict) -> JsonRpcRequestResult:
    return params, None


@app.add_request(method="shutdown", include_server=True)
def shutdown(app: KaiRpcApplication, server: JsonRpcServer) -> tuple[dict, None]:
    server.shutdown_flag = True

    return {}, None


@app.add_request(method="exit", include_server=True)
def exit(app: KaiRpcApplication, server: JsonRpcServer) -> JsonRpcRequestResult:
    server.shutdown_flag = True

    return {}, None


@app.add_request(
    method="initialize", params_model=KaiRpcApplicationConfig, include_server=True
)
def initialize(
    app: KaiRpcApplication, params: KaiRpcApplicationConfig, server: JsonRpcServer
) -> JsonRpcRequestResult:
    if app.initialized:
        return {}, JsonRpcError(
            code=JsonRpcErrorCode.ServerErrorStart,
            message="Server already initialized",
        )

    try:
        app.config = params

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


@app.add_request(method="setConfig", params_model=dict, include_server=True)
def set_config(
    app: KaiRpcApplication, params: dict, server: JsonRpcServer
) -> JsonRpcRequestResult:
    if not app.initialized:
        return {}, ERROR_NOT_INITIALIZED

    # Basically reset everything
    app.initialized = False
    return cast(JsonRpcRequestResult, initialize(app=app, params=params, server=server))


@app.add_request(
    method="getRAGSolution", params_model=PostGetIncidentSolutionsForFileParams
)
def get_rag_solution(
    app: KaiRpcApplication, params: PostGetIncidentSolutionsForFileParams
) -> JsonRpcRequestResult:
    if not app.initialized:
        return {}, ERROR_NOT_INITIALIZED

    # NOTE: This is not at all what we should be doing
    try:
        app.log.info(f"get_rag_solution: {params}")
        params_dict = params.model_dump()
        result = requests.post(
            f"{app.config.kaiBackendUrl}/get_incident_solutions_for_file",
            json=params_dict,
        )
        app.log.info(f"get_rag_solution result: {result}")
        app.log.info(f"get_rag_solution result.json(): {result.json()}")

        return dict(result.json()), None
    except Exception:
        return {}, JsonRpcError(
            code=JsonRpcErrorCode.InternalError,
            message=str(traceback.format_exc()),
        )


@app.add_request(method="getCodeplanAgentSolution", params_model=dict)
def get_codeplan_agent_solution(
    app: KaiRpcApplication, params: dict
) -> JsonRpcRequestResult:
    if not app.initialized:
        return {}, ERROR_NOT_INITIALIZED

    return {
        "result": "Not implemented",
        "message": "Beep boop, I'm a robot",
        "echo": params,
    }, None


# if __name__ == "__main__":
#     # with __import__("ipdb").launch_ipdb_on_exception():
#     file_path = Path(__file__).resolve()
#     docs_path = file_path.parent / "docs.md"
#     print(docs_path)
#     with open(str(docs_path), "w") as f:
#         f.write(app.generate_docs())
