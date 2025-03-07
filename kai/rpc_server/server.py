import os
import platform
import re
import tomllib
import traceback
from contextlib import ExitStack
from itertools import groupby
from operator import attrgetter
from pathlib import Path
from typing import Any, Callable, Generator, Optional, ParamSpec, TypeVar, cast
from unittest.mock import MagicMock
from urllib.parse import urlparse

import yaml
from opentelemetry import trace
from pydantic import BaseModel, ConfigDict

from kai.analyzer import AnalyzerLSP
from kai.analyzer_types import ExtendedIncident, Incident, RuleSet, Violation
from kai.cache import JSONCacheWithTrace
from kai.constants import PATH_LLM_CACHE
from kai.jsonrpc.core import JsonRpcApplication, JsonRpcServer
from kai.jsonrpc.models import JsonRpcError, JsonRpcErrorCode, JsonRpcId
from kai.jsonrpc.util import AutoAbsPath, AutoAbsPathExists, CamelCaseBaseModel
from kai.kai_config import KaiConfigModels
from kai.llm_interfacing.model_provider import ModelProvider
from kai.logging.logging import TRACE, KaiLogConfig, get_logger
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
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager
from kai.reactive_codeplanner.vfs.repo_context_snapshot import RepoContextSnapshot
from kai.rpc_server.chat import Chatter, get_chatter_contextvar

tracer = trace.get_tracer("kai_application")
chatter = get_chatter_contextvar()


class KaiRpcApplicationConfig(CamelCaseBaseModel):
    process_id: Optional[int] = None

    root_path: AutoAbsPath
    model_provider: KaiConfigModels

    log_config: KaiLogConfig

    demo_mode: bool = False
    cache_dir: Optional[AutoAbsPath] = None
    trace_enabled: bool = False
    fail_on_cache_mismatch: bool = False
    enable_reflection: bool = True

    analyzer_lsp_lsp_path: AutoAbsPathExists
    analyzer_lsp_rpc_path: AutoAbsPathExists
    analyzer_lsp_rules_paths: list[AutoAbsPathExists]
    analyzer_lsp_java_bundle_paths: list[AutoAbsPathExists]
    analyzer_lsp_label_selector: Optional[str] = ""
    analyzer_lsp_dep_labels_path: Optional[AutoAbsPathExists] = None
    analyzer_lsp_excluded_paths: Optional[list[AutoAbsPathExists]] = None

    model_config = ConfigDict(protected_namespaces=())

    @staticmethod
    def model_validate_filepath(filepath: str | Path) -> "KaiRpcApplicationConfig":
        """
        Load a model config from a file and validate it.

        Supported file formats:
        - TOML
        - YAML
        - JSON
        """
        model_dict: dict[str, Any]
        _, file_ext = os.path.splitext(filepath)

        if file_ext == ".toml":
            model_dict = tomllib.load(open(filepath, "rb"))
        elif file_ext == ".yaml" or file_ext == ".yml" or file_ext == ".json":
            model_dict = yaml.safe_load(open(filepath, "r"))
        else:
            raise ValueError(f"'{filepath}' has unsupported file type: {file_ext}")

        return KaiRpcApplicationConfig(**model_dict)


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

        if app.config.cache_dir is None:
            app.config.cache_dir = PATH_LLM_CACHE

        try:
            cache = JSONCacheWithTrace(
                cache_dir=app.config.cache_dir,
                model_id="",
                enable_trace=app.config.trace_enabled,
                trace_dir=app.config.log_config.log_dir_path / "traces",
                fail_on_cache_mismatch=app.config.fail_on_cache_mismatch,
            )
            model_provider = ModelProvider.from_config(
                app.config.model_provider, app.config.demo_mode, cache
            )
            cache.model_id = re.sub(r"[\.:\\/]", "_", model_provider.model_id)

            model_provider.validate_environment()
        except Exception as e:
            server.send_response(
                id=id,
                error=JsonRpcError(
                    code=JsonRpcErrorCode.InternalError,
                    message=f"Failed to create model provider: {str(e)}",
                ),
            )
            return

        app.log.info(f"Initialized with config: {app.config}")

        try:
            app.analyzer = AnalyzerLSP(
                analyzer_lsp_server_binary=app.config.analyzer_lsp_rpc_path,
                repo_directory=app.config.root_path,
                rules=app.config.analyzer_lsp_rules_paths,
                java_bundles=app.config.analyzer_lsp_java_bundle_paths,
                analyzer_lsp_path=app.config.analyzer_lsp_lsp_path,
                dep_open_source_labels_path=app.config.analyzer_lsp_dep_labels_path
                or Path(),
                excluded_paths=app.config.analyzer_lsp_excluded_paths,
            )
        except Exception as e:
            server.send_response(
                id=id,
                error=JsonRpcError(
                    code=JsonRpcErrorCode.InternalError,
                    message=f"Failed to start AnalyzerLSP: {str(e)}",
                ),
            )
            return

        internal_config = RpcClientConfig(
            repo_directory=app.config.root_path,
            analyzer_lsp_server_binary=app.config.analyzer_lsp_rpc_path,
            analyzer_rules=app.config.analyzer_lsp_rules_paths,
            analyzer_lsp_path=app.config.analyzer_lsp_lsp_path,
            analyzer_bundle_paths=app.config.analyzer_lsp_java_bundle_paths,
            label_selector=app.config.analyzer_lsp_label_selector,
            incident_selector=None,
            included_paths=None,
            excluded_paths=app.config.analyzer_lsp_excluded_paths,
            dep_open_source_labels_path=app.config.analyzer_lsp_dep_labels_path,
        )

        reflection_agent = None
        if app.config.enable_reflection:
            reflection_agent = ReflectionAgent(
                model_provider=model_provider, iterations=1, retries=3
            )

        app.rcm = RepoContextManager(
            project_root=app.config.root_path,
            reflection_agent=reflection_agent,
        )

        app.log.debug("initialized the repo context manager")

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
@tracer.start_as_current_span("server_analysis_endpoint")
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
            scoped_paths=params.get("scoped_paths", None),
            reset_cache=params.get("reset_cache", None),
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

        return cls(
            work_tree=str(snapshot.work_tree),
            git_dir=str(snapshot.git_dir),
            git_sha=snapshot.git_sha,
            diff=diff,
            msg=snapshot.msg,
            children=[cls.from_snapshot(c) for c in snapshot.children],
            spawning_result=None,
        )


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

    diff = rcm.snapshot.diff(the_snapshot)

    rcm.reset(the_snapshot)

    server.send_response(
        id=id,
        result={
            "diff": diff[1] + diff[2],
        },
    )


class GetCodeplanAgentSolutionParams(BaseModel):
    file_path: Path
    incidents: list[ExtendedIncident]

    max_iterations: Optional[int] = None
    max_depth: Optional[int] = None
    max_priority: Optional[int] = None

    chat_token: str


class GetCodeplanAgentSolutionResult(BaseModel):
    encountered_errors: list[str]
    modified_files: list[str]
    diff: str


@app.add_request(method="getCodeplanAgentSolution")
@tracer.start_as_current_span("get_code_plan_solution")
def get_codeplan_agent_solution(
    app: KaiRpcApplication,
    server: JsonRpcServer,
    id: JsonRpcId,
    params: GetCodeplanAgentSolutionParams,
) -> None:
    # - Create a set of AnalyzerRuleViolations
    # - Seed the task manager with these violations
    # - Get the top task with priority 0 and do the whole loop

    app.log.debug(f"get_codeplan_agent_solution: {params}")
    if not app.initialized or not app.task_manager or not app.rcm:
        server.send_response(id=id, error=ERROR_NOT_INITIALIZED)
        return
    app.config = cast(KaiRpcApplicationConfig, app.config)

    chatter.set(Chatter(server, "my_progress", params.chat_token))

    chatter.get().chat_simple("Getting solution!")

    overall_result = GetCodeplanAgentSolutionResult(
        encountered_errors=[],
        modified_files=[],
        diff="",
    )

    chatter.get().chat_simple("Setting Analysis Cache")
    app.analyzer.run_analyzer_lsp(scoped_paths=app.task_manager.unprocessed_files)
    chatter.get().chat_simple("Analysis Cache Reset")

    # ExitStack calls its callbacks in reverse order upon exiting the with
    # block, **even if an exception is raised**.
    with ExitStack() as defer:
        # Get a snapshot of the current state of the repo so we can reset it
        # later
        app.rcm.commit(
            f"get_codeplan_agent_solution. id: {id}", run_reflection_agent=False
        )
        agent_solution_snapshot = app.rcm.snapshot
        defer.callback(app.rcm.reset, agent_solution_snapshot)

        # TODO: Data for AnalyzerRuleViolation should probably take an
        # ExtendedIncident
        seed_tasks: list[Task] = []

        params.incidents.sort()
        grouped_incidents_by_files = [
            list(g) for _, g in groupby(params.incidents, key=attrgetter("uri"))
        ]
        for incidents in grouped_incidents_by_files:

            # group incidents by violation
            grouped_violations = [
                list(g) for _, g in groupby(incidents, key=attrgetter("violation_name"))
            ]
            for violation_incidents in grouped_violations:

                incident_base = violation_incidents[0]
                uri_path = urlparse(incident_base.uri).path
                if platform.system() == "Windows":
                    uri_path = uri_path.removeprefix("/")

                class_to_use = AnalyzerRuleViolation
                if "pom.xml" in incident_base.uri:
                    class_to_use = AnalyzerDependencyRuleViolation

                validation_error = class_to_use(
                    file=str(Path(uri_path).absolute()),
                    violation=Violation(
                        id=incident_base.violation_name or "",
                        description=incident_base.violation_description or "",
                        category=incident_base.violation_category,
                        labels=incident_base.violation_labels,
                    ),
                    ruleset=RuleSet(
                        name=incident_base.ruleset_name,
                        description=incident_base.ruleset_description or "",
                    ),
                    line=0,
                    column=-1,
                    message="",
                    incidents=[],
                )

                validation_error.incidents = []
                for i in violation_incidents:
                    validation_error.incidents.append(Incident(**i.model_dump()))

                if len(validation_error.incidents) > 0:
                    app.log.log(
                        TRACE,
                        "seed_tasks adding to list: %s -- incident_messages: %s",
                        validation_error,
                        validation_error.incident_message,
                    )
                    seed_tasks.append(validation_error)

        app.task_manager.set_seed_tasks(*seed_tasks)

        app.log.info(
            f"Starting code plan loop with iterations: {params.max_iterations}, max depth: {params.max_depth}, and max priority: {params.max_priority}"
        )

        next_task_fn = scoped_task_fn(
            params.max_iterations, app.task_manager.get_next_task
        )

        initial_solved_tasks = app.task_manager.processed_tasks.copy()
        initial_ignored_tasks = set(app.task_manager.ignored_tasks).copy()

        overall_modified_files: set[str] = set()
        for task in next_task_fn(params.max_priority, params.max_depth):
            app.log.debug(f"Executing task {task.__class__.__name__}: {task}")

            chatter.get().chat_markdown(
                f"Executing task {task.__class__.__name__}."
                f"<details><summary>Details</summary>\n{task.markdown()}</details>\n"
            )

            result = app.task_manager.execute_task(task)

            app.log.debug(f"Task {task.__class__.__name__}, result: {result}")
            chatter.get().chat_markdown(
                f"Finished task {task.__class__.__name__}!"
                f"<details><summary>Details</summary>\n{task.markdown()}</details>\n"
            )

            app.task_manager.supply_result(result)

            app.log.debug(f"Executed task {task.__class__.__name__}")
            app.rcm.commit(f"Executed task {task.__class__.__name__}")

            overall_result.encountered_errors.extend(
                [str(e) for e in result.encountered_errors]
            )
            overall_modified_files = overall_modified_files.union(
                set([str(f) for f in result.modified_files])
            )

            app.log.debug(result)

        overall_result.modified_files = list(overall_modified_files)

        # after we have completed all the tasks, we should show what has been
        # accomplished for this particular solution
        app.log.debug("QUEUE_STATE_END_OF_CODE_PLAN: SUCCESSFUL TASKS: START")
        for task in app.task_manager.processed_tasks - initial_solved_tasks:
            app.log.debug(f"QUEUE_STATE_END_OF_CODE_PLAN: SUCCESSFUL_TASKS: {task}")
        app.log.debug("QUEUE_STATE_END_OF_CODE_PLAN: SUCCESSFUL TASKS: END")
        app.log.debug("QUEUE_STATE_END_OF_CODE_PLAN: IGNORED_TASKS: START")
        for task in set(app.task_manager.ignored_tasks) - initial_ignored_tasks:
            app.log.debug(f"QUEUE_STATE_SEED_TASKS: SUCCESSFUL_TASKS: {task}")
        app.log.debug("QUEUE_STATE_END_OF_CODE_PLAN: IGNORED_TASKS: END")

        msg = f"Finished with {len(overall_result.encountered_errors)} errors and {len(overall_result.modified_files)} modified files.\n"
        if app.task_manager.processed_tasks - initial_solved_tasks:
            msg += "<details><summary>Successful tasks:</summary>\n"
            msg += "<ul>\n"
            for task in app.task_manager.processed_tasks - initial_solved_tasks:
                msg += f"<li>{str(task)}</li>\n"
            msg += "</ul>\n"
            msg += "</details>\n"
        if set(app.task_manager.ignored_tasks) - initial_ignored_tasks:
            msg += "<details><summary>Ignored tasks:</summary>\n"
            msg += "<ul>\n"
            for task in set(app.task_manager.ignored_tasks) - initial_ignored_tasks:
                msg += f"<li>{str(task)}</li>\n"
            msg += "</ul>\n"
            msg += "</details>\n"
        chatter.get().chat_markdown(msg)

        diff = app.rcm.snapshot.diff(agent_solution_snapshot)
        overall_result.diff = diff[1] + diff[2]

        chatter.get().chat_simple("Finished!")

    server.send_response(
        id=id,
        result=overall_result.model_dump(),  # Must dump as a dict for some reason?
    )


P = ParamSpec("P")
R = TypeVar("R")


def scoped_task_fn(
    max_iterations: Optional[int], next_task_fn: Callable[P, Generator[R, Any, None]]
) -> Callable[P, Generator[R, Any, None]]:
    log = get_logger("fn_selection")
    if max_iterations is None:
        log.debug("No max_iterations, returning default get_next_task")
        return next_task_fn

    @tracer.start_as_current_span("scoped_task")
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
