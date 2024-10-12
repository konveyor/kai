import logging
import sys
import traceback
from pathlib import Path
from typing import Optional, cast
from urllib.parse import urlparse

import requests
from pydantic import BaseModel

from kai.models.kai_config import KaiConfigModels
from kai.routes.get_incident_solutions_for_file import (
    PostGetIncidentSolutionsForFileParams,
)
from kai.service.kai_application.kai_application import UpdatedFileContent
from kai.service.llm_interfacing.model_provider import ModelProvider
from playpen.repo_level_awareness.agent.reflection_agent import ReflectionAgent
from playpen.repo_level_awareness.api import RpcClientConfig, TaskResult
from playpen.repo_level_awareness.codeplan import TaskManager
from playpen.repo_level_awareness.task_runner.analyzer_lsp.task_runner import (
    AnalyzerTaskRunner,
)
from playpen.repo_level_awareness.task_runner.analyzer_lsp.validator import (
    AnalyzerLSPStep,
)
from playpen.repo_level_awareness.vfs.git_vfs import (
    RepoContextManager,
    RepoContextSnapshot,
)
from playpen.rpc.core import JsonRpcApplication, JsonRpcServer
from playpen.rpc.logs import JsonRpcLoggingHandler
from playpen.rpc.models import JsonRpcError, JsonRpcErrorCode, JsonRpcId
from playpen.rpc.util import DEFAULT_FORMATTER, TRACE, CamelCaseBaseModel


class KaiRpcApplicationConfig(CamelCaseBaseModel):
    process_id: Optional[int]

    root_uri: str
    kantra_uri: str
    analyzer_lsp_uri: str
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


@app.add_request(method="echo")
def echo(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict
) -> None:
    server.send_response(id=id, result=params)


@app.add_request(method="shutdown")
def shutdown(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict
) -> None:
    server.shutdown_flag = True

    server.send_response(id=id, result={})


@app.add_request(method="exit")
def exit(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict
) -> None:
    server.shutdown_flag = True

    server.send_response(id=id, result={})


@app.add_request(method="initialize")
def initialize(
    app: KaiRpcApplication,
    server: JsonRpcServer,
    id: JsonRpcId,
    params: KaiRpcApplicationConfig,
) -> None:
    if app.initialized:
        server.send_response(
            id=id,
            error=JsonRpcError(
                code=JsonRpcErrorCode.ServerErrorStart,
                message="Server already initialized",
            ),
        )
        return

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
        server.send_response(
            id=id,
            error=JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message=str(e),
            ),
        )
        return

    app.initialized = True

    server.send_response(id=id, result={})


@app.add_request(method="setConfig")
def set_config(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict
) -> None:
    if not app.initialized:
        server.send_response(id=id, error=ERROR_NOT_INITIALIZED)
        return
    app.config = cast(KaiRpcApplicationConfig, app.config)

    # Basically reset everything
    app.initialized = False
    try:
        initialize.func(app, server, id, KaiRpcApplicationConfig.model_validate(params))
    except Exception as e:
        server.send_response(
            id=id,
            error=JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message=str(e),
            ),
        )


@app.add_request(method="getRAGSolution")
def get_rag_solution(
    app: KaiRpcApplication,
    server: JsonRpcServer,
    id: JsonRpcId,
    params: PostGetIncidentSolutionsForFileParams,
) -> None:
    if not app.initialized:
        server.send_response(id=id, error=ERROR_NOT_INITIALIZED)
        return
    app.config = cast(KaiRpcApplicationConfig, app.config)

    # NOTE: This is not at all what we should be doing
    try:
        app.log.info(f"get_rag_solution: {params}")
        params_dict = params.model_dump()
        result = requests.post(
            f"{app.config.kai_backend_url}/get_incident_solutions_for_file",
            json=params_dict,
            timeout=1024,
        )
        app.log.info(f"get_rag_solution result: {result}")
        app.log.info(f"get_rag_solution result.json(): {result.json()}")

        server.send_response(id=id, result=dict(result.json()))
    except Exception:
        server.send_response(
            id=id,
            error=JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message=str(traceback.format_exc()),
            ),
        )


class GetCodeplanAgentSolutionParams(BaseModel):
    file_path: Path

    # For demo only
    replacing_file_path: Path


class GitVFSUpdateParams(BaseModel):
    work_tree: Path  # project root
    git_dir: Path
    git_sha: str
    diff: str

    children: list["GitVFSUpdateParams"]

    @classmethod
    def from_snapshot(cls, snapshot: RepoContextSnapshot) -> "GitVFSUpdateParams":
        return cls(
            work_tree=snapshot.work_tree,
            git_dir=snapshot.git_dir,
            git_sha=snapshot.git_sha,
            diff=snapshot.diff(snapshot.parent)[1] if snapshot.parent else "",
            children=[cls.from_snapshot(c) for c in snapshot.children],
        )

    # spawning_result: Optional[SpawningResult] = None


@app.add_request(method="getCodeplanAgentSolution")
def get_codeplan_agent_solution(
    app: KaiRpcApplication,
    server: JsonRpcServer,
    id: JsonRpcId,
    params: GetCodeplanAgentSolutionParams,
) -> None:
    app.log.info(f"get_codeplan_agent_solution: {params}")
    if not app.initialized:
        server.send_response(id=id, error=ERROR_NOT_INITIALIZED)
        return

    app.config = cast(KaiRpcApplicationConfig, app.config)

    try:
        model_provider = ModelProvider(app.config.model_provider)
    except Exception as e:
        server.send_response(
            id=id,
            error=JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message=str(e),
            ),
        )
        return

    # NOTE(JonahSussman): I don't think the reflection agent should be used in
    # the RCM, I Feel like it should be just like another agent, but that
    # produces tasks with a high priority
    ReflectionAgent(llm=model_provider.llm, iterations=1, retries=3)

    rcm = RepoContextManager(
        project_root=Path(urlparse(app.config.root_uri).path),
    )

    replaced_file_content = open(params.replacing_file_path).read()
    with open(params.file_path, "w") as f:
        f.write(replaced_file_content)

    rcm.commit("Replaced file content")
    server.send_notification(
        "gitVFSUpdate", GitVFSUpdateParams.from_snapshot(rcm.first_snapshot)
    )

    updated_file_content = UpdatedFileContent(
        updated_file=replaced_file_content,
        total_reasoning=[],
        used_prompts=[],
        model_id=model_provider.model_id,
        additional_information=[],
        llm_results=None,
    )

    # TODO: It'd be nice to unify these config classes
    task_manager_config = RpcClientConfig(
        repo_directory=Path(urlparse(app.config.root_uri).path),
        analyzer_lsp_server_binary=Path(urlparse(app.config.analyzer_lsp_uri).path),
        rules_directory=Path(urlparse(app.config.analyzer_lsp_uri).path) / "rules",
        label_selector=None,
        incident_selector=None,
        included_paths=None,
    )

    task_manager = TaskManager(
        config=task_manager_config,
        rcm=rcm,
        updated_file_content=updated_file_content,
        validators=[
            # MavenCompileStep(task_manager_config),
            AnalyzerLSPStep(task_manager_config),
        ],
        agents=[
            AnalyzerTaskRunner(model_provider.llm),
            # MavenCompilerTaskRunner(model_provider.llm),
        ],
    )

    result: TaskResult
    for task in task_manager.get_next_task():
        app.log.debug(f"Executing task {task.__class__.__name__}")

        result = task_manager.execute_task(task)
        app.log.debug(f"Task {task.__class__.__name__} result: {result}")

        task_manager.supply_result(result)

        app.log.debug(f"Executed task {task.__class__.__name__}")
        rcm.commit(f"Executed task {task.__class__.__name__}")
        server.send_notification(
            "gitVFSUpdate", GitVFSUpdateParams.from_snapshot(rcm.first_snapshot)
        )

    task_manager.stop()

    diff = rcm.snapshot.git(
        ["diff", f"{rcm.snapshot.git_sha}", f"{rcm.first_snapshot.git_sha}"]
    )[1]

    rcm.reset_to_first()

    server.send_response(
        id=id,
        result={
            "encountered_errors": [str(e) for e in result.encountered_errors],
            "modified_files": [str(f) for f in result.modified_files],
            "diff": diff,
        },
    )
