import traceback
from pathlib import Path
from typing import (
    Any,
    Callable,
    Generator,
    Optional,
    ParamSpec,
    TypedDict,
    TypeVar,
    cast,
)
from unittest.mock import MagicMock
from urllib.parse import urlparse

from opentelemetry import trace
from pydantic import BaseModel

from kai.analyzer import AnalyzerLSP
from kai.analyzer_types import ExtendedIncident, Incident, RuleSet, Violation
from kai.constants import PATH_LLM_CACHE
from kai.jsonrpc.core import JsonRpcApplication, JsonRpcServer
from kai.jsonrpc.models import JsonRpcError, JsonRpcErrorCode, JsonRpcId
from kai.jsonrpc.util import CamelCaseBaseModel
from kai.kai_config import KaiConfigModels, SolutionConsumerKind
from kai.llm_interfacing.model_provider import ModelProvider
from kai.logging.logging import KaiLogger, get_logger
from kai.reactive_codeplanner.agent.analyzer_fix.agent import AnalyzerAgent
from kai.reactive_codeplanner.agent.dependency_agent.dependency_agent import (
    MavenDependencyAgent,
)
from kai.reactive_codeplanner.agent.maven_compiler_fix.agent import MavenCompilerAgent
from kai.reactive_codeplanner.agent.reflection_agent import ReflectionAgent
from kai.reactive_codeplanner.task_manager.api import RpcClientConfig, Task
from kai.reactive_codeplanner.task_manager.task_manager import TaskManager
from kai.reactive_codeplanner.task_runner.analyzer_lsp.api import (
    AnalyzerDependencyRuleViolation,
    AnalyzerRuleViolation,
)
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

tracer = trace.get_tracer("kai_application")


class KaiRpcApplicationConfig(CamelCaseBaseModel):
    process_id: Optional[int]

    root_path: Path
    model_provider: KaiConfigModels
    solution_consumer: SolutionConsumerKind = SolutionConsumerKind.DIFF_ONLY
    kai_backend_url: str

    log_level: str = "INFO"
    stderr_log_level: str = "TRACE"
    file_log_level: Optional[str] = None
    log_dir_path: Optional[Path] = None
    demo_mode: bool = False
    cache_dir: Optional[Path]

    analyzer_lsp_lsp_path: Path
    analyzer_lsp_rpc_path: Path
    analyzer_lsp_rules_path: Path
    analyzer_lsp_java_bundle_path: Path
    analyzer_lsp_dep_labels_path: Optional[Path] = None


class KaiRpcApplication(JsonRpcApplication):
    analyzer: AnalyzerLSP

    def __init__(self) -> None:
        super().__init__()

        self.initialized = False
        self.config: Optional[KaiRpcApplicationConfig] = None
        self.log = get_logger("kai_rpc_application")
        self.analysis_validator: Optional[AnalyzerLSPStep] = None
        self.task_manager: Optional[TaskManager] = None
        self.rcm: Optional[RepoContextManager] = None


app = KaiRpcApplication()

ERROR_NOT_INITIALIZED = JsonRpcError(
    code=JsonRpcErrorCode.ServerErrorStart,
    message="Server not initialized",
)


@app.add_request(method="echo")
@tracer.start_as_current_span("echo")
def echo(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
) -> None:
    server.send_response(id=id, result=params)


@app.add_request(method="shutdown")
@tracer.start_as_current_span("shutdown")
def shutdown(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
) -> None:
    server.shutdown_flag = True
    if app.analyzer is not None:
        app.analyzer.stop()
    server.send_response(id=id, result={})


@app.add_request(method="exit")
@tracer.start_as_current_span("exit")
def exit(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
) -> None:
    server.shutdown_flag = True
    if app.analyzer is not None:
        app.analyzer.stop()
    server.send_response(id=id, result={})


# NOTE(shawn-hurley): would it ever make sense to have the server
# "re-initialized" or would you just shutdown and restart the process?
@app.add_request(method="initialize")
@tracer.start_as_current_span("initialize")
def initialize(
    app: KaiRpcApplication,
    server: JsonRpcServer,
    id: JsonRpcId,
    params: KaiRpcApplicationConfig,
    log: Optional[KaiLogger] = None,
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
        if app.config.log_dir_path:
            app.config.log_dir_path = app.config.log_dir_path.resolve()
        if app.config.analyzer_lsp_dep_labels_path:
            app.config.analyzer_lsp_dep_labels_path = (
                app.config.analyzer_lsp_dep_labels_path.resolve()
            )
        app.config.analyzer_lsp_rpc_path = app.config.analyzer_lsp_rpc_path.resolve()
        app.config.analyzer_lsp_java_bundle_path = (
            app.config.analyzer_lsp_java_bundle_path.resolve()
        )
        app.config.analyzer_lsp_lsp_path = app.config.analyzer_lsp_lsp_path.resolve()
        app.config.analyzer_lsp_rules_path = (
            app.config.analyzer_lsp_rules_path.resolve()
        )
        if app.config.cache_dir is not None:
            app.config.cache_dir = app.config.cache_dir.resolve()
        else:
            app.config.cache_dir = Path(PATH_LLM_CACHE)

        try:
            model_provider = ModelProvider(
                app.config.model_provider, app.config.demo_mode, app.config.cache_dir
            )
        except Exception as e:
            app.log.error("unable to get model provider:", e)
            raise

        app.log.info(f"Initialized with config: {app.config}")

        app.analyzer = AnalyzerLSP(
            analyzer_lsp_server_binary=app.config.analyzer_lsp_rpc_path,
            repo_directory=app.config.root_path,
            rules_directory=app.config.analyzer_lsp_rules_path,
            analyzer_lsp_path=app.config.analyzer_lsp_lsp_path,
            analyzer_java_bundle_path=app.config.analyzer_lsp_java_bundle_path,
            dep_open_source_labels_path=app.config.analyzer_lsp_dep_labels_path
            or Path(),
        )

        internal_config = RpcClientConfig(
            repo_directory=app.config.root_path,
            analyzer_lsp_server_binary=app.config.analyzer_lsp_rpc_path,
            rules_directory=app.config.analyzer_lsp_rules_path,
            analyzer_lsp_path=app.config.analyzer_lsp_lsp_path,
            analyzer_java_bundle_path=app.config.analyzer_lsp_java_bundle_path,
            label_selector="konveyor.io/target=quarkus || konveyor.io/target=jakarta-ee",
            incident_selector=None,
            included_paths=None,
            dep_open_source_labels_path=app.config.analyzer_lsp_dep_labels_path,
        )

        app.rcm = RepoContextManager(
            project_root=app.config.root_path,
            reflection_agent=ReflectionAgent(
                model_provider=model_provider, iterations=1, retries=3
            ),
        )

        app.log.debug("initalized the repo context manager")

        # Right now this is not usable by anything.
        # server.send_notification(
        #     "gitVFSUpdate",
        #     GitVFSUpdateParams.from_snapshot(rcm.first_snapshot).model_dump(),
        # )

        if app.analysis_validator is None:
            app.log.debug("creating analyzer LSP Step")
            app.analysis_validator = AnalyzerLSPStep(internal_config, app.analyzer)

        app.task_manager = TaskManager(
            config=internal_config,
            rcm=app.rcm,
            validators=[
                MavenCompileStep(internal_config),
                app.analysis_validator,
            ],
            task_runners=[
                AnalyzerTaskRunner(AnalyzerAgent(model_provider)),
                MavenCompilerTaskRunner(MavenCompilerAgent(model_provider)),
                DependencyTaskRunner(
                    MavenDependencyAgent(model_provider, app.config.root_path)
                ),
            ],
        )

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
@tracer.start_as_current_span("set_config")
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


@app.add_request(method="analysis_engine.Analyze")
def analyze(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
) -> None:
    if not app.initialized:
        server.send_response(id=id, error=ERROR_NOT_INITIALIZED)
        return

    try:
        analyzer_output = app.analyzer.run_analyzer_lsp(
            label_selector=params.get("label_selector", ""),
            included_paths=params.get("included_paths", []),
            incident_selector=params.get("incident_selector", ""),
        )

        if isinstance(analyzer_output, JsonRpcError):
            server.send_response(
                id=id,
                error=JsonRpcError(
                    code=JsonRpcErrorCode.InternalError,
                    message=analyzer_output.message,
                ),
            )
            return

        if analyzer_output is None:
            server.send_response(
                id=id,
                error=JsonRpcError(
                    code=JsonRpcErrorCode.UnknownErrorCode,
                    message="Analyzer output is unexpectedly empty",
                ),
            )
            return

        if analyzer_output.result is None:
            server.send_response(
                id=id,
                error=JsonRpcError(
                    code=JsonRpcErrorCode.UnknownErrorCode,
                    message="Analysis result unexpectedly empty",
                ),
            )
            return

        if isinstance(analyzer_output.result, BaseModel):
            server.send_response(id=id, result=analyzer_output.result.model_dump())
            return

        server.send_response(id=id, result=analyzer_output.result)
    except Exception as e:
        server.send_response(
            id=id,
            error=JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message=str(e),
            ),
        )


class GetRagSolutionParams(BaseModel):
    file_path: Path
    incidents: list[ExtendedIncident]
    trace_enabled: bool = False
    include_solved_incidents: bool = False


class GetCodeplanAgentSolutionParams(BaseModel):
    file_path: Path
    incidents: list[ExtendedIncident]

    max_iterations: Optional[int] = None
    max_depth: Optional[int] = None
    max_priority: Optional[int] = None


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
            model_provider=MagicMock(),
        ),
    )

    with open(params.file_path, "w") as f:
        f.write(params.new_content)

    rcm.commit("testRCM")
    the_snapshot = rcm.snapshot

    diff = rcm.snapshot.diff(rcm.first_snapshot)

    rcm.reset(the_snapshot)

    server.send_response(
        id=id,
        result={
            "diff": diff[1] + diff[2],
        },
    )


@app.add_request(method="getCodeplanAgentSolution")
@tracer.start_as_current_span("get_codeplan_solution")
def get_codeplan_agent_solution(
    app: KaiRpcApplication,
    server: JsonRpcServer,
    id: JsonRpcId,
    params: GetCodeplanAgentSolutionParams,
) -> None:
    try:
        # create a set of AnalyzerRuleViolations
        # seed the task manager with these violations
        # get the task with priority 0 and do the whole thingy

        app.log.debug(f"get_codeplan_agent_solution: {params}")
        if not app.initialized or not app.task_manager or not app.rcm:
            server.send_response(id=id, error=ERROR_NOT_INITIALIZED)
            return

        # Get a snapshot of the current state of the repo so we can reset it
        # later
        app.rcm.commit(
            f"get_codeplan_agent_solution. id: {id}", run_reflection_agent=False
        )
        agent_solution_snapshot = app.rcm.snapshot

        app.config = cast(KaiRpcApplicationConfig, app.config)

        # Data for AnalyzerRuleViolation should probably take an ExtendedIncident
        seed_tasks: list[Task] = []

        for incident in params.incidents:

            class_to_use = AnalyzerRuleViolation
            if "pom.xml" in incident.uri:
                class_to_use = AnalyzerDependencyRuleViolation
            seed_tasks.append(
                class_to_use(
                    file=urlparse(incident.uri).path,
                    line=incident.line_number,
                    column=-1,  # Not contained within report?
                    message=incident.message,
                    priority=0,
                    incident=Incident(**incident.model_dump()),
                    violation=Violation(
                        id=incident.violation_name or "",
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
        app.task_manager.set_seed_tasks(*seed_tasks)

        app.log.info(f"get_codeplan_agent_solution: {seed_tasks}")

        app.log.info(
            f"starting code plan loop with iterations: {params.max_iterations}, max depth: {params.max_depth}, and max priority: {params.max_priority}"
        )
        next_task_fn = scoped_task_fn(
            params.max_iterations, app.task_manager.get_next_task
        )

        class OverallResult(TypedDict):
            encountered_errors: list[str]
            modified_files: list[str]
            diff: str

        overall_result: OverallResult = {
            "encountered_errors": [],
            "modified_files": [],
            "diff": "",
        }

        for task in next_task_fn(params.max_priority, params.max_depth):
            app.log.debug(f"Executing task {task.__class__.__name__}: {task}")

            result = app.task_manager.execute_task(task)

            app.log.debug(f"Task {task.__class__.__name__} result: {result}")

            app.task_manager.supply_result(result)

            app.log.debug(f"Executed task {task.__class__.__name__}")
            app.rcm.commit(f"Executed task {task.__class__.__name__}")

            overall_result["encountered_errors"].extend(
                [str(e) for e in result.encountered_errors]
            )
            overall_result["modified_files"].extend(
                [str(f) for f in result.modified_files]
            )

            app.log.debug(result)
            app.log.debug("QUEUE_STATE: START")
            try:
                queue_state = str(app.task_manager.priority_queue)
                for line in queue_state.splitlines():
                    app.log.debug(f"QUEUE_STATE: {line}")
            except Exception as e:
                app.log.error(f"QUEUE_STATE: {e}")
            app.log.debug("QUEUE_STATE: END")
            app.log.debug("QUEUE_STATE: SUCCESSFUL_TASKS: START")
            for task in app.task_manager.processed_tasks:
                app.log.debug(f"QUEUE_STATE: SUCCESSFUL_TASKS: {task}")
            app.log.debug("QUEUE_STATE: SUCCESSFUL_TASKS: END")
            app.log.debug("QUEUE_STATE: IGNORED_TASKS: START")
            for task in app.task_manager.ignored_tasks:
                app.log.debug(f"QUEUE_STATE: IGNORED_TASKS: {task}")
            app.log.debug("QUEUE_STATE: IGNORED_TASKS: END")

        diff = app.rcm.snapshot.diff(app.rcm.first_snapshot)
        overall_result["diff"] = diff[1] + diff[2]

        app.rcm.reset(agent_solution_snapshot)

        server.send_response(
            id=id,
            result=dict(overall_result),
        )
    except Exception as e:
        if app.rcm is not None:
            app.rcm.reset(agent_solution_snapshot)

        app.log.error(e)
        raise


P = ParamSpec("P")
R = TypeVar("R")


def scoped_task_fn(
    max_iterations: Optional[int], next_task_fn: Callable[P, Generator[R, Any, None]]
) -> Callable[P, Generator[R, Any, None]]:
    log = get_logger("fn_selection")
    if max_iterations is None:
        log.debug("No max_iterations, returning default get_next_task")
        return next_task_fn

    def inner(*args: P.args, **kwargs: P.kwargs) -> Generator[R, Any, None]:
        log.info(f"In inner {args}, {kwargs}")
        generator = next_task_fn(*args, **kwargs)
        for i in range(max_iterations):
            try:
                log.debug(f"Yielding on iteration {i}")
                yield next(generator)
            except StopIteration:
                break

    log.debug("Returning the iteration-scoped get_next_task function")

    return inner
