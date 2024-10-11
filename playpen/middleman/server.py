import logging
import sys
import traceback
from pathlib import Path
from typing import Any, Optional, cast
from urllib.parse import urlparse

import requests
from pydantic import AliasChoices, AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from kai.models.kai_config import KaiConfigModels
from kai.routes.get_incident_solutions_for_file import (
    PostGetIncidentSolutionsForFileParams,
)
from kai.service.llm_interfacing.model_provider import ModelProvider
from playpen.repo_level_awareness.api import RpcClientConfig
from playpen.rpc.core import JsonRpcApplication, JsonRpcServer
from playpen.rpc.logs import JsonRpcLoggingHandler
from playpen.rpc.models import JsonRpcError, JsonRpcErrorCode, JsonRpcRequestResult
from playpen.rpc.util import DEFAULT_FORMATTER, TRACE, CamelCaseBaseModel

log = logging.getLogger(__name__)


class KaiRpcApplicationConfig(CamelCaseBaseModel):
    process_id: Optional[int]

    root_uri: str
    kantra_uri: str
    model_provider: KaiConfigModels
    kai_backend_url: str

    log_level: str = "INFO"
    stderr_log_level: str = "TRACE"
    file_log_level: Optional[str] = None
    log_dir_uri: Optional[str] = None


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
        notify_handler.setLevel(app.config.log_level)
        notify_handler.setFormatter(DEFAULT_FORMATTER)
        app.log.addHandler(notify_handler)

        if app.config.file_log_level and app.config.log_dir_uri:
            log_dir = Path(app.config.log_dir_uri)  # FIXME: urlparse?
            log_file = log_dir / "kai_rpc.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(app.config.file_log_level)
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
            f"{app.config.kai_backend_url}/get_incident_solutions_for_file",
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


class GetCodeplanAgentSolutionParams(BaseModel):
    pass


@app.add_request(
    method="getCodeplanAgentSolution", params_model=GetCodeplanAgentSolutionParams
)
def get_codeplan_agent_solution(
    app: KaiRpcApplication, params: GetCodeplanAgentSolutionParams
) -> JsonRpcRequestResult:
    if not app.initialized:
        return {}, ERROR_NOT_INITIALIZED

    try:
        model_provider = ModelProvider(app.config.model_provider)
    except Exception as e:
        return {}, JsonRpcError(
            code=JsonRpcErrorCode.InternalError,
            message=str(e),
        )

    # TODO: It'd be nice to unify these config classes
    task_manager_config = RpcClientConfig(
        repo_directory=Path(urlparse(app.config.root_uri).path),
    )
