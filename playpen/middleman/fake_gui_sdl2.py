"""
NOTE(JonahSussman): This is probably some of the ugliest code that I have ever
written in my entire life. I am so sorry.

The main goal with this code is to create a fake GUI that can be used to
interact with the RPC server. This is useful for testing purposes, as it allows
us to rapidly iterate on the RPC server without needing to interface with the
IDE.
"""

import ctypes
import json
import os
import subprocess  # trunk-ignore(bandit/B404)
import sys
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BufferedReader, BufferedWriter
from pathlib import Path
from types import NoneType
from typing import IO, Any, Callable, Union, cast, get_args, get_origin
from urllib.parse import urlparse

import imgui  # type: ignore[import-untyped]
import OpenGL.GL as gl  # type: ignore[import-untyped]
import yaml
from imgui.integrations.sdl2 import SDL2Renderer  # type: ignore[import-untyped]
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from sdl2 import (  # type: ignore[import-untyped]
    SDL_GL_ACCELERATED_VISUAL,
    SDL_GL_CONTEXT_FLAGS,
    SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG,
    SDL_GL_CONTEXT_MAJOR_VERSION,
    SDL_GL_CONTEXT_MINOR_VERSION,
    SDL_GL_CONTEXT_PROFILE_CORE,
    SDL_GL_CONTEXT_PROFILE_MASK,
    SDL_GL_DEPTH_SIZE,
    SDL_GL_DOUBLEBUFFER,
    SDL_GL_MULTISAMPLEBUFFERS,
    SDL_GL_MULTISAMPLESAMPLES,
    SDL_GL_STENCIL_SIZE,
    SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK,
    SDL_HINT_VIDEO_HIGHDPI_DISABLED,
    SDL_INIT_EVERYTHING,
    SDL_QUIT,
    SDL_WINDOW_OPENGL,
    SDL_WINDOW_RESIZABLE,
    SDL_WINDOWPOS_CENTERED,
    SDL_CreateWindow,
    SDL_DestroyWindow,
    SDL_Event,
    SDL_GetError,
    SDL_GL_CreateContext,
    SDL_GL_DeleteContext,
    SDL_GL_MakeCurrent,
    SDL_GL_SetAttribute,
    SDL_GL_SetSwapInterval,
    SDL_GL_SwapWindow,
    SDL_Init,
    SDL_PollEvent,
    SDL_Quit,
    SDL_SetHint,
)

from kai.models.kai_config import KaiConfigModels
from kai.models.report import Report
from kai.models.report_types import ExtendedIncident
from kai.models.util import remove_known_prefixes
from kai.routes.get_incident_solutions_for_file import (
    PostGetIncidentSolutionsForFileParams,
)
from playpen.middleman.server import (
    GetCodeplanAgentSolutionParams,
    GitVFSUpdateParams,
    KaiRpcApplicationConfig,
    get_codeplan_agent_solution,
    initialize,
)
from playpen.rpc.callbacks import JsonRpcCallback
from playpen.rpc.core import JsonRpcApplication, JsonRpcServer
from playpen.rpc.models import JsonRpcId
from playpen.rpc.streams import BareJsonStream

THIS_FILE_PATH = Path(os.path.abspath(__file__)).resolve()
THIS_DIR_PATH = THIS_FILE_PATH.parent
KAI_DIR = THIS_DIR_PATH.parent.parent


class Drawable(ABC):
    def __init__(self, *, show: bool = True) -> None:
        self.show = show

    def draw(self) -> None:
        if self.show:
            self._draw()

    @abstractmethod
    def _draw(self) -> None: ...


CONFIG = KaiRpcApplicationConfig(
    process_id=os.getpid(),
    root_path=KAI_DIR / "example/coolstore",
    analyzer_lsp_path=KAI_DIR / "analyzer-lsp",
    analyzer_lsp_rpc_path=KAI_DIR / "analyzer-lsp",
    model_provider=KaiConfigModels(
        provider="ChatIBMGenAI",
        args={
            "model_id": "meta-llama/llama-3-70b-instruct",
        },
    ),
    kai_backend_url="http://localhost:8080",
    log_level="TRACE",
)


class ConfigurationEditor(Drawable):
    def __init__(self, params: list[tuple[str, BaseModel]]) -> None:
        super().__init__()

        self.params: dict[str, tuple[BaseModel, dict[str, Any]]] = {}
        for method, the_params in params:
            self.params[method] = (the_params, json.loads(the_params.model_dump_json()))

    def _draw(self) -> None:
        _, self.show = imgui.begin("Configuration Editor", closable=True)

        if imgui.begin_tab_bar("ConfigurationEditorTabBar"):
            for method in self.params:
                if imgui.begin_tab_item(method).selected:
                    self.draw_tab(method)
                    imgui.end_tab_item()

            imgui.end_tab_bar()

        imgui.end()

    def draw_tab(self, method: str) -> None:
        params, extra = self.params[method]
        fields = params.model_fields

        if imgui.button(f"Populate `{method}` request"):
            JSON_RPC_REQUEST_WINDOW.rpc_kind_n = 0
            JSON_RPC_REQUEST_WINDOW.rpc_method = method

            try:
                JSON_RPC_REQUEST_WINDOW.rpc_params = params.__class__.model_validate(
                    params.model_dump()
                ).model_dump_json(
                    indent=2,
                )
            except Exception as e:
                JSON_RPC_REQUEST_WINDOW.rpc_params = f"Error parsing JSON: {e}"

            imgui.set_window_focus_labeled("JSON RPC Request Window")

        for field_name in fields:
            field = fields[field_name]
            self.draw_field(
                params,
                extra,
                field_name,
                # field,
                field_annotation=field.annotation,
            )

    def draw_field(
        self,
        params: BaseModel,
        extra: dict[str, Any],
        field_name: str,
        # field: FieldInfo,
        field_annotation: Any,
    ) -> None:
        if get_origin(field_annotation) is Union:
            args = get_args(field_annotation)
            combo_items_key = field_name + "_combo_items"
            combo_current_key = field_name + "_combo_current"

            if combo_items_key not in extra:
                extra[combo_items_key] = [arg.__name__ for arg in args]

            if combo_current_key not in extra:
                selected_index = next(
                    (
                        i
                        for i, arg in enumerate(args)
                        if arg == getattr(params, field_name).__class__
                    ),
                    -1,
                )
                extra[combo_current_key] = selected_index

            _, extra[combo_current_key] = imgui.combo(
                label=field_name + " type",
                current=extra[combo_current_key],
                items=extra[combo_items_key],
            )

            self.draw_field(
                params,
                extra,
                field_name,
                field_annotation=args[extra[combo_current_key]],
            )
        elif field_annotation is None or field_annotation is NoneType:
            setattr(params, field_name, None)
        elif field_annotation is str:
            _, result = imgui.input_text(
                field_name, str(getattr(params, field_name)), 400
            )
            setattr(params, field_name, result)
        elif field_annotation is Path:
            _, result = imgui.input_text(
                field_name, str(getattr(params, field_name)), 400
            )
            setattr(params, field_name, result)
        elif field_annotation is int:
            attr = getattr(params, field_name)
            if not isinstance(attr, int):
                attr = 0

            _, result = imgui.input_int(field_name, attr)
            setattr(params, field_name, result)
        elif field_annotation is float:
            attr = getattr(params, field_name)
            if not isinstance(attr, float):
                attr = 0.0

            _, result = imgui.input_float(field_name, attr)
            setattr(params, field_name, result)
        elif field_annotation is bool:
            _, result = imgui.checkbox(field_name, bool(getattr(params, field_name)))
            setattr(params, field_name, result)
        elif field_annotation is dict:
            dict_key = field_name + "_dict"
            if dict_key not in extra:
                extra[dict_key] = "{}"

            try:
                extra[dict_key] = json.dumps(getattr(params, field_name))
            except Exception:
                pass

            imgui.text(field_name)
            _, extra[dict_key] = imgui.input_text_multiline(
                field_name, extra[dict_key], 4096 * 16
            )

            try:
                setattr(params, field_name, json.loads(extra[dict_key]))
            except Exception as e:
                setattr(params, field_name, e)

        elif issubclass(field_annotation, BaseModel):
            imgui.text(field_name)

            imgui.indent()

            for sub_field_name in field_annotation.model_fields:
                sub_field = field_annotation.model_fields[sub_field_name]
                self.draw_field(
                    getattr(params, field_name),
                    extra,
                    sub_field_name,
                    field_annotation=sub_field.annotation,
                )

            imgui.unindent()
        else:
            imgui.text(f"Unknown type. {field_name}: {field_annotation}")


class SourceEditor(Drawable):
    def __init__(self) -> None:
        super().__init__()

        self.application_path = "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/example/coolstore"
        self.relative_filename = (
            "/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java"
        )
        self.report_path = "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/example/analysis/coolstore/output.yaml"

        self.relative_filename_path: Path | None = None
        self.file_path: Path | None = None

        self.editor_content = ""
        self.report: Report | None = None
        self.incidents: dict[int, ExtendedIncident] = {}

    def _draw(self) -> None:

        window_name = "Source Code Editor"
        if self.file_path:
            window_name += f" - {self.relative_filename}"

        _, self.show = imgui.begin(
            window_name, flags=imgui.WINDOW_MENU_BAR, closable=True
        )

        if imgui.begin_menu_bar():
            if imgui.begin_menu("File"):
                clicked, FILE_LOADER.show = imgui.menu_item(
                    "Load File/Analysis Report", selected=FILE_LOADER.show
                )
                imgui.end_menu()
            imgui.end_menu_bar()

        for line_number, line in enumerate(self.editor_content.split("\n"), 1):
            if line_number in self.incidents:
                incident = self.incidents[line_number]

                # imgui.same_line()
                imgui.text_colored(f"{line_number:4d}: {line}", 1.0, 0.0, 0.0)
                # imgui.text_colored(f" [Issue: {highlighted_lines[idx]['message']}] ", 1.0, 0.0, 0.0)

                # Hover message
                if imgui.is_item_hovered():
                    imgui.begin_tooltip()

                    imgui.text_colored(incident.ruleset_name, 1.0, 0.0, 0.0)
                    imgui.text_colored(incident.violation_name, 1.0, 0.0, 0.0)
                    imgui.separator()
                    imgui.text(incident.message)
                    imgui.end_tooltip()

                # Context menu
                if imgui.is_item_clicked(imgui.MOUSE_BUTTON_RIGHT):
                    imgui.open_popup(f"context_menu_{line_number}")

                if imgui.begin_popup(f"context_menu_{line_number}"):
                    if imgui.begin_menu("Populate..."):
                        if imgui.selectable("getRAGSolution")[0]:
                            JSON_RPC_REQUEST_WINDOW.rpc_kind_n = 0
                            JSON_RPC_REQUEST_WINDOW.rpc_method = "getRAGSolution"
                            JSON_RPC_REQUEST_WINDOW.rpc_params = json.dumps(
                                PostGetIncidentSolutionsForFileParams(
                                    file_name=str(self.file_path),
                                    file_contents=self.editor_content,
                                    application_name="coolstore",
                                    incidents=[incident],
                                ).model_dump(),
                                indent=2,
                            )

                            imgui.set_window_focus_labeled("JSON RPC Request Window")

                        if imgui.selectable("getCodeplanAgentSolution")[0]:
                            JSON_RPC_REQUEST_WINDOW.rpc_kind_n = 0
                            JSON_RPC_REQUEST_WINDOW.rpc_method = (
                                "getCodeplanAgentSolution"
                            )
                            JSON_RPC_REQUEST_WINDOW.rpc_params = json.dumps(
                                {
                                    "file_name": str(self.file_path),
                                    "file_contents": self.editor_content,
                                    "application_name": "coolstore",
                                    "incidents": [incident.model_dump()],
                                },
                                indent=2,
                            )

                            imgui.set_window_focus_labeled("JSON RPC Request Window")

                        imgui.end_menu()
                    imgui.end_popup()
            else:
                imgui.text(f"{line_number:4d}: {line}")

        imgui.end()


class FileLoader(Drawable):
    def __init__(self) -> None:
        super().__init__()
        self.show = False

    def _draw(self) -> None:
        if not self.show:
            return

        _, self.show = imgui.begin("File Loader", closable=True)

        imgui.text("Load File/Analysis Report")
        _, SOURCE_EDITOR.application_path = imgui.input_text(
            "Application Path", SOURCE_EDITOR.application_path, 400
        )
        _, SOURCE_EDITOR.relative_filename = imgui.input_text(
            "Filename", SOURCE_EDITOR.relative_filename, 400
        )
        _, SOURCE_EDITOR.report_path = imgui.input_text(
            "Report", SOURCE_EDITOR.report_path, 400
        )

        if imgui.button("Load"):
            application_path = Path(SOURCE_EDITOR.application_path).resolve()
            parts = Path(SOURCE_EDITOR.relative_filename).resolve().parts
            while len(parts) > 0 and parts[0] == "/":
                parts = parts[1:]

            SOURCE_EDITOR.relative_filename_path = Path(*parts)
            SOURCE_EDITOR.file_path = application_path.joinpath(*parts)
            SOURCE_EDITOR.editor_content = self.load_file()
            SOURCE_EDITOR.incidents = self.load_analysis_report()

            self.show = False

        imgui.end()

    def load_file(self) -> str:
        if SOURCE_EDITOR.file_path is None:
            return ""

        with open(SOURCE_EDITOR.file_path, "r") as file:
            return file.read()

    def load_analysis_report(self) -> dict[Any, Any]:
        report = Report.load_report_from_file(SOURCE_EDITOR.report_path)
        result = {}

        for ruleset_name, ruleset in report.rulesets.items():
            for violation_name, violation in ruleset.violations.items():
                for incident in violation.incidents:
                    if report.should_we_skip_incident(incident):
                        continue

                    file_path = Path(remove_known_prefixes(urlparse(incident.uri).path))
                    if file_path != SOURCE_EDITOR.relative_filename_path:
                        print(f"{SOURCE_EDITOR.relative_filename} != {file_path}")
                        continue

                    result[incident.line_number] = ExtendedIncident(
                        ruleset_name=ruleset_name,
                        violation_name=violation_name,
                        ruleset_description=ruleset.description,
                        violation_description=violation.description,
                        **incident.model_dump(),
                    )

        return result

        # NOTE: Break glass in case of emergency

        # return {
        #     1: ExtendedIncident(
        #         uri=f"file://{SOURCE_EDITOR.file_path}",
        #         message="This is a test incident",
        #         code_snip="print('Hello, world!')",
        #         line_number=1,
        #         variables={},
        #         ruleset_name="test ruleset",
        #         violation_name="test violation",
        #     ),
        # }


class JsonRpcRequestWindow(Drawable):
    def __init__(self) -> None:
        super().__init__()

        self.rpc_kind_items = ["Request", "Notification"]
        self.rpc_kind_n = 0
        self.rpc_method = ""
        self.rpc_params = ""

    @property
    def rpc_kind(self) -> str:
        return self.rpc_kind_items[self.rpc_kind_n]

    def _draw(self) -> None:
        _, self.show = imgui.begin("JSON RPC Request Window", closable=True)

        _, self.rpc_kind_n = imgui.combo(
            label="Kind", current=self.rpc_kind_n, items=self.rpc_kind_items
        )
        _, self.rpc_method = imgui.input_text("Method", self.rpc_method, 512)
        _, self.rpc_params = imgui.input_text_multiline(
            "Params", self.rpc_params, 4096 * 16
        )

        if imgui.button("Submit"):
            submit_json_rpc_request(self.rpc_kind, self.rpc_method, self.rpc_params)

        imgui.end()


class RequestResponseInspector(Drawable):
    def __init__(self) -> None:
        super().__init__()

        self.selected_indices: dict[Any, Any] = {}

    def _draw(self) -> None:
        _, self.show = imgui.begin("Request/Response Inspector", closable=True)

        if imgui.begin_tab_bar("RequestsTabBar"):

            if imgui.begin_tab_item("Requests").selected:

                if imgui.begin_table(
                    "Requests", 3, imgui.TABLE_RESIZABLE | imgui.TABLE_SCROLL_Y
                ):
                    imgui.table_setup_column("ID")
                    imgui.table_setup_column("Request")
                    imgui.table_setup_column("Response")
                    imgui.table_headers_row()

                    for entry in json_rpc_responses:
                        imgui.table_next_column()
                        if imgui.selectable(str(entry["request"]["id"]))[0]:
                            self.selected_indices[entry["request"]["id"]] = entry

                        imgui.table_next_column()
                        if imgui.selectable(str(entry["request"]))[0]:
                            self.selected_indices[entry["request"]["id"]] = entry
                        if imgui.is_item_hovered():
                            imgui.begin_tooltip()
                            imgui.text(yaml.dump(entry["request"]))
                            imgui.end_tooltip()

                        imgui.table_next_column()

                        if imgui.selectable(str(entry["response"]))[0]:
                            self.selected_indices[entry["request"]["id"]] = entry
                        if imgui.is_item_hovered():
                            imgui.begin_tooltip()
                            imgui.text(yaml.dump(entry["response"]))
                            imgui.end_tooltip()

                    imgui.end_table()
                imgui.end_tab_item()

            for idx, entry in self.selected_indices.items():
                if imgui.begin_tab_item(f"Request {idx}").selected:
                    imgui.text("Request")

                    imgui.begin_child(
                        "scrollable request",
                        border=True,
                        flags=imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR
                        | imgui.WINDOW_HORIZONTAL_SCROLLING_BAR,
                    )
                    lines = yaml.dump(entry).split("\n")
                    for line in lines:
                        imgui.text(line)
                    imgui.end_child()

                    # imgui.separator()

                    # imgui.text("Response")

                    # imgui.begin_child("scrollable response", border=True, flags=imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR | imgui.WINDOW_HORIZONTAL_SCROLLING_BAR)
                    # imgui.text(yaml.dump(entry["response"]))
                    # imgui.end_child()

                    imgui.end_tab_item()

            imgui.end_tab_bar()

        imgui.end()


class SubprocessInspector(Drawable):
    def __init__(self) -> None:
        super().__init__()

        self.scroll_to_bottom = False

    def _draw(self) -> None:
        global rpc_subprocess_stderr_log

        _, self.show = imgui.begin("Subprocess Manager", closable=True)

        if rpc_subprocess is None:
            if imgui.button("Start"):
                start_server(["python", rpc_script_path])
        else:
            if imgui.button("Stop"):
                stop_server()

        imgui.same_line()
        if imgui.button("Clear log"):
            rpc_subprocess_stderr_log.clear()

        imgui.text("Subprocess stderr log:")

        imgui.begin_child(
            "scrollable_region",
            border=True,
            flags=imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR
            | imgui.WINDOW_HORIZONTAL_SCROLLING_BAR,
        )

        if self.scroll_to_bottom:
            self.scroll_to_bottom = False

        for log_line in rpc_subprocess_stderr_log:
            imgui.text(log_line)
        imgui.end_child()

        imgui.end()


rpc_application: JsonRpcApplication = JsonRpcApplication()

GIT_VFS_UPDATE_PARAMS: GitVFSUpdateParams = None


@rpc_application.add_notify(method="gitVFSUpdate")
def handle_git_vfs_update(
    app: JsonRpcApplication,
    server: JsonRpcServer,
    id: JsonRpcId,
    params: GitVFSUpdateParams,
) -> None:
    global GIT_VFS_UPDATE_PARAMS

    GIT_VFS_UPDATE_PARAMS = params


class GitVFSInspector(Drawable):
    def __init__(self) -> None:
        super().__init__()

    def _draw(self) -> None:
        _, self.show = imgui.begin("Git VFS Inspector", closable=True)

        if GIT_VFS_UPDATE_PARAMS is None:
            imgui.text("No gitVFSUpdate notification received.")
        else:
            imgui.text("gitVFSUpdate notification received.")
            imgui.text(yaml.dump(GIT_VFS_UPDATE_PARAMS.model_dump()))

        imgui.end()


# Global variables

SOURCE_EDITOR = SourceEditor()
FILE_LOADER = FileLoader()
JSON_RPC_REQUEST_WINDOW = JsonRpcRequestWindow()
REQUEST_RESPONSE_INSPECTOR = RequestResponseInspector()
SUBPROCESS_INSPECTOR = SubprocessInspector()
GIT_VFS_INSPECTOR = GitVFSInspector()

CONFIGURATION_EDITOR = ConfigurationEditor(
    params=[
        ("initialize", CONFIG),
        (
            "getCodeplanAgentSolution",
            GetCodeplanAgentSolutionParams(
                file_path=Path(
                    "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/example/coolstore/src/main/java/com/redhat/coolstore/model/InventoryEntity.java"
                ),
                replacing_file_path=Path(
                    "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/notebooks/compilation_agent/testing_field_type_change_errors/CatalogItemEntity.java"
                ),
            ),
        ),
    ]
)

# CONFIGURATION_EDITOR = ConfigurationEditorOld()

json_rpc_responses = []
rpc_subprocess_stderr_log = []
rpc_subprocess = None

rpc_script_path = Path(os.path.dirname(os.path.realpath(__file__))) / "main.py"
rpc_server: JsonRpcServer = None


def start_server(command: list[str]) -> None:
    global rpc_subprocess
    global rpc_subprocess_stderr_log
    global rpc_server

    # trunk-ignore-begin(bandit/B603)
    rpc_subprocess = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # trunk-ignore-end(bandit/B603)

    rpc_subprocess_stderr_log.append("Subprocess started.")

    def read_stderr() -> None:
        global rpc_subprocess_stderr_log

        while True:
            stderr_line = cast(IO[bytes], rpc_subprocess.stderr).readline()
            if stderr_line:
                rpc_subprocess_stderr_log.append(stderr_line.decode("utf-8").strip())
                SUBPROCESS_INSPECTOR.scroll_to_bottom = True
            else:
                break

    threading.Thread(target=read_stderr, daemon=True).start()

    rpc_server = JsonRpcServer(
        json_rpc_stream=BareJsonStream(
            cast(BufferedReader, rpc_subprocess.stdout),
            cast(BufferedWriter, rpc_subprocess.stdin),
        ),
        request_timeout=None,
        app=rpc_application,
    )
    rpc_server.start()


def stop_server() -> None:
    global rpc_subprocess
    global rpc_server
    global rpc_subprocess_stderr_log

    if rpc_subprocess:
        rpc_subprocess.terminate()
        rpc_subprocess = None
        rpc_subprocess_stderr_log.append("Subprocess terminated.")

        rpc_server.stop()


def submit_json_rpc_request(kind: str, method: str, params: Any) -> None:
    global rpc_server

    try:
        params_dict = json.loads(params)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return

    def asyncly_send_request() -> None:
        table_request = {
            "method": method,
            "params": params_dict,
        }

        if kind == "Request":
            table_request["id"] = rpc_server.next_id

        idx = len(json_rpc_responses)
        json_rpc_responses.append(
            {"kind": kind, "request": table_request, "response": None}
        )

        if kind == "Request":
            response = rpc_server.send_request(method, params_dict)
        elif kind == "Notification":
            json_rpc_responses.append(
                {"kind": kind, "request": table_request, "response": None}
            )

            response = None
        else:
            raise ValueError(f"Invalid RPC kind: {kind}")

        if response is None:
            json_rpc_responses[idx]["response"] = {"note": "Response is None"}
        else:
            json_rpc_responses[idx]["response"] = response.model_dump(
                exclude={"jsonrpc"}
            )

    threading.Thread(target=asyncly_send_request).start()


# Main loop
def main() -> None:
    window, gl_context = impl_pysdl2_init()

    imgui.create_context()
    impl = SDL2Renderer(window)
    imgui_io = imgui.get_io()
    imgui_io.fonts.add_font_default()
    imgui_io.font_global_scale = 1
    imgui.style_colors_dark()

    event = SDL_Event()
    running = True
    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()

        imgui.begin_main_menu_bar()

        if imgui.begin_menu("View"):
            clicked, SOURCE_EDITOR.show = imgui.menu_item(
                "Source Editor", selected=SOURCE_EDITOR.show
            )
            clicked, JSON_RPC_REQUEST_WINDOW.show = imgui.menu_item(
                "JSON RPC Request Window", selected=JSON_RPC_REQUEST_WINDOW.show
            )
            clicked, REQUEST_RESPONSE_INSPECTOR.show = imgui.menu_item(
                "Request/Response Inspector", selected=REQUEST_RESPONSE_INSPECTOR.show
            )
            clicked, SUBPROCESS_INSPECTOR.show = imgui.menu_item(
                "Subprocess Inspector", selected=SUBPROCESS_INSPECTOR.show
            )
            clicked, CONFIGURATION_EDITOR.show = imgui.menu_item(
                "Configuration Editor", selected=CONFIGURATION_EDITOR.show
            )
            clicked, GIT_VFS_INSPECTOR.show = imgui.menu_item(
                "Git VFS Inspector", selected=GIT_VFS_INSPECTOR.show
            )
            imgui.end_menu()

        imgui.end_main_menu_bar()

        SOURCE_EDITOR.draw()
        FILE_LOADER.draw()
        JSON_RPC_REQUEST_WINDOW.draw()
        REQUEST_RESPONSE_INSPECTOR.draw()
        SUBPROCESS_INSPECTOR.draw()
        CONFIGURATION_EDITOR.draw()
        GIT_VFS_INSPECTOR.draw()

        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        SDL_GL_SwapWindow(window)

    impl.shutdown()
    SDL_GL_DeleteContext(gl_context)
    SDL_DestroyWindow(window)
    SDL_Quit()


def impl_pysdl2_init() -> tuple[int, Any]:
    width, height = 1280, 720
    window_name = "Fake GUI for RPC Server"

    if SDL_Init(SDL_INIT_EVERYTHING) < 0:
        print(
            "Error: SDL could not initialize! SDL Error: "
            + SDL_GetError().decode("utf-8")
        )
        sys.exit(1)

    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_ACCELERATED_VISUAL, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 8)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 4)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)

    SDL_SetHint(SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK, b"1")
    SDL_SetHint(SDL_HINT_VIDEO_HIGHDPI_DISABLED, b"1")

    window = SDL_CreateWindow(
        window_name.encode("utf-8"),
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        width,
        height,
        SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE,
    )

    if window is None:
        print(
            "Error: Window could not be created! SDL Error: "
            + SDL_GetError().decode("utf-8")
        )
        sys.exit(1)

    gl_context = SDL_GL_CreateContext(window)
    if gl_context is None:
        print(
            "Error: Cannot create OpenGL Context! SDL Error: "
            + SDL_GetError().decode("utf-8")
        )
        sys.exit(1)

    SDL_GL_MakeCurrent(window, gl_context)
    if SDL_GL_SetSwapInterval(1) < 0:
        print(
            "Warning: Unable to set VSync! SDL Error: " + SDL_GetError().decode("utf-8")
        )
        sys.exit(1)

    return window, gl_context


if __name__ == "__main__":
    main()
