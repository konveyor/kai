import ctypes
import json
import os
import queue
import subprocess
import sys
import threading
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.parse import urlparse

import imgui
import OpenGL.GL as gl
import yaml
from imgui.integrations.sdl2 import SDL2Renderer
from sdl2 import *

from kai.models.kai_config import KaiConfigModels
from kai.models.report import Report
from kai.models.report_types import ExtendedIncident
from kai.models.util import remove_known_prefixes
from kai.routes.get_incident_solutions_for_file import (
    PostGetIncidentSolutionsForFileParams,
)
from playpen.middleman.server import KaiRpcApplicationConfig
from playpen.rpc.core import JsonRpcServer
from playpen.rpc.streams import BareJsonStream

THIS_FILE_PATH = Path(os.path.abspath(__file__)).resolve()
THIS_DIR_PATH = THIS_FILE_PATH.parent
KAI_DIR = THIS_DIR_PATH.parent.parent


class Drawable(ABC):
    def __init__(self, *, show: bool = True):
        self.show = show

    def draw(self):
        if self.show:
            self._draw()

    @abstractmethod
    def _draw(self): ...


CONFIG = KaiRpcApplicationConfig(
    process_id=os.getpid(),
    root_uri=f"file://{KAI_DIR / 'example/coolstore'}",
    kantra_uri=f"file://{KAI_DIR / 'kantra'}",
    model_provider=KaiConfigModels(
        provider="ChatIBMGenAI",
        args={
            "model_id": "meta-llama/llama-3-70b-instruct",
        },
    ),
    kai_backend_url="http://localhost:8080",
)


class ConfigurationEditor(Drawable):
    def __init__(self):
        super().__init__()

    @property
    def model_args(self):
        return json.dumps(CONFIG.model_provider.args)

    @model_args.setter
    def model_args(self, value):
        CONFIG.model_provider.args = json.loads(value)

    def _draw(self):
        _, self.show = imgui.begin("Configuration Editor", closable=True)

        imgui.text("Configuration Editor")

        imgui.input_int(
            "Process ID", CONFIG.process_id, flags=imgui.INPUT_TEXT_READ_ONLY
        )
        _, CONFIG.root_uri = imgui.input_text("Root URI", CONFIG.root_uri, 400)
        _, CONFIG.kantra_uri = imgui.input_text("Kantra URI", CONFIG.kantra_uri, 400)
        _, CONFIG.kai_backend_url = imgui.input_text(
            "Kai Backend URL", CONFIG.kai_backend_url, 400
        )
        _, CONFIG.model_provider.provider = imgui.input_text(
            "Model Provider", CONFIG.model_provider.provider, 400
        )
        _, self.model_args = imgui.input_text("Model Args", self.model_args, 400)

        if imgui.button("Populate `initialize` request"):
            JSON_RPC_REQUEST_WINDOW.rpc_kind_n = 0
            JSON_RPC_REQUEST_WINDOW.rpc_method = "initialize"
            JSON_RPC_REQUEST_WINDOW.rpc_params = json.dumps(
                CONFIG.model_dump(), indent=2
            )

            imgui.set_window_focus_labeled("JSON RPC Request Window")

        imgui.end()


class SourceEditor(Drawable):
    def __init__(self):
        super().__init__()

        self.application_path = "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/example/coolstore"
        self.relative_filename = (
            "/src/main/java/com/redhat/coolstore/service/OrderServiceMDB.java"
        )
        self.report_path = "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/example/analysis/coolstore/output.yaml"

        self.relative_filename_path: Path = None
        self.file_path: Path = None

        self.editor_content = ""
        self.report: Report = None
        self.incidents: dict[int, ExtendedIncident] = {}

    def _draw(self):

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
    def __init__(self):
        super().__init__()
        self.show = False

    def _draw(self):
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

    def load_file(self):
        with open(SOURCE_EDITOR.file_path, "r") as file:
            return file.read()

    def load_analysis_report(self):
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
    def __init__(self):
        super().__init__()

        self.rpc_kind_items = ["Request", "Notification"]
        self.rpc_kind_n = 0
        self.rpc_method = ""
        self.rpc_params = ""

    @property
    def rpc_kind(self):
        return self.rpc_kind_items[self.rpc_kind_n]

    def _draw(self):
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
    def __init__(self):
        super().__init__()

        self.selected_indices = dict()

    def _draw(self):
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
    def __init__(self):
        super().__init__()

    def _draw(self):
        _, self.show = imgui.begin("Subprocess Manager", closable=True)

        if rpc_subprocess is None:
            if imgui.button("Start"):
                start_server(["python", rpc_script_path])
        else:
            if imgui.button("Stop"):
                stop_server()

        imgui.text("Subprocess stderr log:")

        imgui.begin_child(
            "scrollable_region",
            border=True,
            flags=imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR
            | imgui.WINDOW_HORIZONTAL_SCROLLING_BAR,
        )
        for log_line in rpc_subprocess_stderr_log:
            imgui.text(log_line)
        imgui.end_child()

        imgui.end()


# Global variables

SOURCE_EDITOR = SourceEditor()
FILE_LOADER = FileLoader()
JSON_RPC_REQUEST_WINDOW = JsonRpcRequestWindow()
REQUEST_RESPONSE_INSPECTOR = RequestResponseInspector()
SUBPROCESS_INSPECTOR = SubprocessInspector()
CONFIGURATION_EDITOR = ConfigurationEditor()

json_rpc_responses = []
rpc_subprocess_stderr_log = []
rpc_subprocess = None

rpc_script_path = Path(os.path.dirname(os.path.realpath(__file__))) / "main.py"
rpc_server: JsonRpcServer = None


def start_server(command):
    global rpc_subprocess
    global rpc_subprocess_stderr_log
    global rpc_server

    rpc_subprocess = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    rpc_subprocess_stderr_log.append("Subprocess started.")

    def read_stderr():
        global rpc_subprocess_stderr_log
        while True:
            stderr_line = rpc_subprocess.stderr.readline()
            if stderr_line:
                rpc_subprocess_stderr_log.append(stderr_line.decode("utf-8").strip())
            else:
                break

    threading.Thread(target=read_stderr, daemon=True).start()

    rpc_server = JsonRpcServer(
        json_rpc_stream=BareJsonStream(
            rpc_subprocess.stdout,
            rpc_subprocess.stdin,
        ),
        request_timeout=None,
    )
    rpc_server.start()


def stop_server():
    global rpc_subprocess
    global rpc_server
    global rpc_subprocess_stderr_log

    if rpc_subprocess:
        rpc_subprocess.terminate()
        rpc_subprocess = None
        rpc_subprocess_stderr_log.append("Subprocess terminated.")

        rpc_server.stop()


def submit_json_rpc_request(kind, method, params):
    global rpc_server

    try:
        params_dict = json.loads(params)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return

    def asyncly_send_request():
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

            response = rpc_server.send_notification(method, params_dict)
        else:
            raise ValueError(f"Invalid RPC kind: {kind}")

        json_rpc_responses[idx]["response"] = response.model_dump(exclude="jsonrpc")

    threading.Thread(target=asyncly_send_request).start()


# Main loop
def main():
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
            imgui.end_menu()

        imgui.end_main_menu_bar()

        SOURCE_EDITOR.draw()
        FILE_LOADER.draw()
        JSON_RPC_REQUEST_WINDOW.draw()
        REQUEST_RESPONSE_INSPECTOR.draw()
        SUBPROCESS_INSPECTOR.draw()
        CONFIGURATION_EDITOR.draw()

        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        SDL_GL_SwapWindow(window)

    impl.shutdown()
    SDL_GL_DeleteContext(gl_context)
    SDL_DestroyWindow(window)
    SDL_Quit()


def impl_pysdl2_init():
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
