import logging
import sys
import threading
import traceback
from pathlib import Path
from typing import Any, Optional, cast
from unittest.mock import MagicMock
from urllib.parse import urlparse

from pydantic import BaseModel

from kai.analyzer_types import ExtendedIncident, Incident, RuleSet, Violation
from kai.jsonrpc.core import JsonRpcApplication, JsonRpcServer
from kai.jsonrpc.logs import JsonRpcLoggingHandler
from kai.jsonrpc.models import JsonRpcError, JsonRpcErrorCode, JsonRpcId
from kai.jsonrpc.util import CamelCaseBaseModel
from kai.kai_config import KaiConfigModels
from kai.logging.logging import TRACE, formatter, get_logger
from kai.reactive_codeplanner.agent.dependency_agent.dependency_agent import (
    MavenDependencyAgent,
)
from kai.reactive_codeplanner.agent.reflection_agent import ReflectionAgent
from kai.reactive_codeplanner.task_manager.api import RpcClientConfig, Task, TaskResult
from kai.reactive_codeplanner.task_manager.task_manager import TaskManager
from kai.reactive_codeplanner.task_runner.analyzer_lsp.api import AnalyzerRuleViolation
from kai.reactive_codeplanner.task_runner.analyzer_lsp.task_runner import (
    AnalyzerTaskRunner,
)
from kai.reactive_codeplanner.task_runner.analyzer_lsp.validator import AnalyzerLSPStep
from kai.reactive_codeplanner.task_runner.compiler.compiler_task_runner import (
    MavenCompilerTaskRunner,
)
from kai.reactive_codeplanner.task_runner.compiler.maven_validator import (
    MavenCompileStep,
)
from kai.reactive_codeplanner.task_runner.dependency.task_runner import (
    DependencyTaskRunner,
)
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager, RepoContextSnapshot
from kai_solution_server.service.llm_interfacing.model_provider import ModelProvider


class KaiRpcApplicationConfig(CamelCaseBaseModel):
    process_id: Optional[int]

    root_path: Path
    model_provider: KaiConfigModels
    kai_backend_url: str

    log_level: str = "INFO"
    stderr_log_level: str = "TRACE"
    file_log_level: Optional[str] = None
    log_dir_path: Optional[Path] = None

    analyzer_lsp_lsp_path: Path
    analyzer_lsp_rpc_path: Path
    analyzer_lsp_rules_path: Path
    analyzer_lsp_java_bundle_path: Path


class KaiRpcApplication(JsonRpcApplication):
    def __init__(self) -> None:
        super().__init__()

        self.initialized = False
        self.config: Optional[KaiRpcApplicationConfig] = None
        self.log = get_logger("kai_rpc_application")


app = KaiRpcApplication()

ERROR_NOT_INITIALIZED = JsonRpcError(
    code=JsonRpcErrorCode.ServerErrorStart,
    message="Server not initialized",
)


@app.add_request(method="echo")
def echo(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
) -> None:
    server.send_response(id=id, result=params)


@app.add_request(method="shutdown")
def shutdown(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
) -> None:
    server.shutdown_flag = True

    server.send_response(id=id, result={})


@app.add_request(method="exit")
def exit(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
) -> None:
    server.shutdown_flag = True

    server.send_response(id=id, result={})


# NOTE(shawn-hurley): would it ever make sense to have the server
# "re-initialized" or would you just shutdown and restart the process?
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

        app.config.root_path = app.config.root_path.resolve()
        app.config.analyzer_lsp_rpc_path = app.config.analyzer_lsp_rpc_path.resolve()
        if app.config.log_dir_path:
            app.config.log_dir_path = app.config.log_dir_path.resolve()

        app.log.setLevel(TRACE)
        app.log.handlers.clear()
        app.log.filters.clear()

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(TRACE)
        stderr_handler.setFormatter(formatter)
        app.log.addHandler(stderr_handler)

        notify_handler = JsonRpcLoggingHandler(server)
        notify_handler.setLevel(app.config.log_level)
        notify_handler.setFormatter(formatter)
        app.log.addHandler(notify_handler)

        if app.config.file_log_level and app.config.log_dir_path:
            log_file = app.config.log_dir_path / "kai_rpc.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(app.config.file_log_level)
            file_handler.setFormatter(formatter)
            app.log.addHandler(file_handler)

        app.log.info(f"Initialized with config: {app.config}")

    except Exception:
        server.send_response(
            id=id,
            error=JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message=str(traceback.format_exc()),
            ),
        )
        return

    app.initialized = True

    server.send_response(id=id, result=app.config.model_dump())


# NOTE(shawn-hurley): I would just as soon make this another initialize call
# rather than a separate endpoint. but open to others feedback.
@app.add_request(method="setConfig")
def set_config(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
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


# @app.add_request(method="getRAGSolution")
# def get_rag_solution(
#     app: KaiRpcApplication,
#     server: JsonRpcServer,
#     id: JsonRpcId,
#     params: PostGetIncidentSolutionsForFileParams,
# ) -> None:
#     if not app.initialized:
#         server.send_response(id=id, error=ERROR_NOT_INITIALIZED)
#         return
#     app.config = cast(KaiRpcApplicationConfig, app.config)

#     # NOTE: This is not at all what we should be doing
#     try:
#         app.log.info(f"get_rag_solution: {params}")
#         params_dict = params.model_dump()
#         result = requests.post(
#             f"{app.config.kai_backend_url}/get_incident_solutions_for_file",
#             json=params_dict,
#             timeout=1024,
#         )
#         app.log.info(f"get_rag_solution result: {result}")
#         app.log.info(f"get_rag_solution result.json(): {result.json()}")

#         server.send_response(id=id, result=dict(result.json()))
#     except Exception:
#         server.send_response(
#             id=id,
#             error=JsonRpcError(
#                 code=JsonRpcErrorCode.InternalError,
#                 message=str(traceback.format_exc()),
#             ),
#         )


class GetCodeplanAgentSolutionParams(BaseModel):
    file_path: Path
    incidents: list[ExtendedIncident]


class GitVFSUpdateParams(BaseModel):
    work_tree: str  # project root
    git_dir: str
    git_sha: str
    diff: str
    msg: str
    spawning_result: Optional[str]

    children: list["GitVFSUpdateParams"]

    @classmethod
    def from_snapshot(cls, snapshot: RepoContextSnapshot) -> "GitVFSUpdateParams":
        if snapshot.parent:
            diff_result = snapshot.diff(snapshot.parent)
            diff = diff_result[1] + diff_result[2]
        else:
            diff = ""

        try:
            spawning_result = repr(snapshot.spawning_result)
        except Exception:
            spawning_result = ""

        return cls(
            work_tree=str(snapshot.work_tree),
            git_dir=str(snapshot.git_dir),
            git_sha=snapshot.git_sha,
            diff=diff,
            msg=snapshot.msg,
            children=[cls.from_snapshot(c) for c in snapshot.children],
            spawning_result=spawning_result,
        )

    # spawning_result: Optional[SpawningResult] = None


class TestRCMParams(BaseModel):
    rcm_root: Path
    file_path: Path
    new_content: str


@app.add_request(method="testRCM")
def test_rcm(
    app: KaiRpcApplication,
    server: JsonRpcServer,
    id: JsonRpcId,
    params: TestRCMParams,
) -> None:
    rcm = RepoContextManager(
        project_root=params.rcm_root,
        reflection_agent=ReflectionAgent(
            llm=MagicMock(),
        ),
    )

    with open(params.file_path, "w") as f:
        f.write(params.new_content)

    rcm.commit("testRCM")

    diff = rcm.snapshot.diff(rcm.first_snapshot)

    rcm.reset_to_first()

    server.send_response(
        id=id,
        result={
            "diff": diff[1] + diff[2],
        },
    )


@app.add_request(method="getCodeplanAgentSolution")
def get_codeplan_agent_solution(
    app: KaiRpcApplication,
    server: JsonRpcServer,
    id: JsonRpcId,
    params: GetCodeplanAgentSolutionParams,
) -> None:
    # create a set of AnalyzerRuleViolations
    # seed the task manager with these violations
    # get the task with priority 0 and do the whole thingy

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

    # Data for AnalyzerRuleViolation should probably take an ExtendedIncident
    seed_tasks: list[Task] = []

    for incident in params.incidents:
        seed_tasks.append(
            AnalyzerRuleViolation(
                file=urlparse(incident.uri).path,
                line=incident.line_number,
                column=-1,  # Not contained within report?
                message=incident.message,
                priority=0,
                incident=Incident(**incident.model_dump()),
                violation=Violation(
                    description=incident.violation_description or "",
                    category=incident.violation_category,
                    labels=incident.violation_labels,
                ),
                ruleset=RuleSet(
                    name=incident.ruleset_name,
                    description=incident.ruleset_description or "",
                ),
            )
        )

    rcm = RepoContextManager(
        project_root=app.config.root_path,
        reflection_agent=ReflectionAgent(
            llm=model_provider.llm, iterations=1, retries=3
        ),
    )

    server.send_notification(
        "gitVFSUpdate",
        GitVFSUpdateParams.from_snapshot(rcm.first_snapshot).model_dump(),
    )

    task_manager_config = RpcClientConfig(
        repo_directory=app.config.root_path,
        analyzer_lsp_server_binary=app.config.analyzer_lsp_rpc_path,
        rules_directory=app.config.analyzer_lsp_rules_path,
        analyzer_lsp_path=app.config.analyzer_lsp_lsp_path,
        analyzer_java_bundle_path=app.config.analyzer_lsp_java_bundle_path,
        label_selector="konveyor.io/target=quarkus || konveyor.io/target=jakarta-ee",
        incident_selector=None,
        included_paths=None,
    )

    task_manager = TaskManager(
        config=task_manager_config,
        rcm=rcm,
        seed_tasks=seed_tasks,
        validators=[
            MavenCompileStep(task_manager_config),
            AnalyzerLSPStep(task_manager_config),
        ],
        agents=[
            AnalyzerTaskRunner(model_provider.llm),
            MavenCompilerTaskRunner(model_provider.llm),
            DependencyTaskRunner(
                MavenDependencyAgent(model_provider.llm, app.config.root_path)
            ),
        ],
    )

    num_loops = 0
    result: TaskResult
    for task in task_manager.get_next_task(0):
        if num_loops == 2:
            break

        app.log.debug(f"Executing task {task.__class__.__name__}: {task}")

        result = task_manager.execute_task(task)

        app.log.debug(f"Task {task.__class__.__name__} result: {result}")

        task_manager.supply_result(result)

        app.log.debug(f"Executed task {task.__class__.__name__}")
        rcm.commit(f"Executed task {task.__class__.__name__}")

        server.send_notification(
            "gitVFSUpdate",
            GitVFSUpdateParams.from_snapshot(rcm.first_snapshot).model_dump(),
        )

        num_loops += 1

    # FIXME: This is a hack to stop the task_manager as it's hanging trying to stop everything
    threading.Thread(target=task_manager.stop).start()

    diff = rcm.snapshot.diff(rcm.first_snapshot)

    rcm.reset_to_first()

    server.send_response(
        id=id,
        result={
            "encountered_errors": [str(e) for e in result.encountered_errors],
            "modified_files": [str(f) for f in result.modified_files],
            "diff": diff[1] + diff[2],
        },
    )
