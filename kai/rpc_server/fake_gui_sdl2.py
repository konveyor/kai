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
from enum import Enum
from io import BufferedReader, BufferedWriter
from pathlib import Path
from types import NoneType
from typing import IO, Any, TypeVar, Union, cast, get_args, get_origin
from urllib.parse import urlparse

import imgui  # type: ignore[import-untyped]
import OpenGL.GL as gl  # type: ignore[import-untyped]
import yaml
from imgui.integrations.sdl2 import SDL2Renderer  # type: ignore[import-untyped]
from pydantic import BaseModel, ValidationError
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

from kai.jsonrpc.core import JsonRpcApplication, JsonRpcServer
from kai.jsonrpc.models import JsonRpcId
from kai.jsonrpc.streams import BareJsonStream
from kai.models.kai_config import KaiConfigModels
from kai.models.report import Report
from kai.models.report_types import Category, ExtendedIncident
from kai.models.util import remove_known_prefixes
from kai.rpc_server.server import (
    GetCodeplanAgentSolutionParams,
    GitVFSUpdateParams,
    KaiRpcApplicationConfig,
    TestRCMParams,
)

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


def try_construct_base_model(cls: type[BaseModelT]) -> BaseModelT:
    inp: dict[Any, Any] = {}

    def set_field(d: dict[Any, Any], loc: tuple[int | str, ...], value: Any) -> None:
        if len(loc) == 1:
            d[loc[0]] = value
        else:
            d[loc[0]] = {}
            set_field(d[loc[0]], loc[1:], value)

    while True:
        try:
            obj = cls.model_validate(inp)
            return obj
        except ValidationError as validation_error:
            for err in validation_error.errors():
                if err["type"] == "missing":
                    set_field(inp, err["loc"], None)
                elif err["type"] == "string_type":
                    set_field(inp, err["loc"], "")
                else:
                    print(err)
                    exit(1)


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
    analyzer_lsp_lsp_path=Path(
        "/home/jonah/.vscode/extensions/redhat.java-1.35.1-linux-x64/server/bin/jdtls"
    ),
    analyzer_lsp_rpc_path=KAI_DIR / "analyzer-lsp",
    analyzer_lsp_rules_path=Path(
        "/home/jonah/Projects/github.com/konveyor/rulesets/default/generated"
    ),
    analyzer_lsp_java_bundle_path=Path(
        "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/notebooks/kai-analyzer-code-plan/java-bundle/java-analyzer-bundle.core-1.0.0-SNAPSHOT.jar"
    ),
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
    def __init__(self, method_and_params: list[tuple[str, BaseModel]]) -> None:
        super().__init__()

        self.model_and_extra: dict[str, tuple[BaseModel, dict[str, Any]]] = {}
        for method, params in method_and_params:
            self.model_and_extra[method] = (params, {})

        print(self.model_and_extra)

    def set_params(
        self, method: str, params: BaseModel, extra: dict[str, Any] | None = None
    ) -> None:
        if extra is None:
            extra = {}

        self.model_and_extra[method] = (params, extra)

    def _draw(self) -> None:
        _, self.show = imgui.begin("Configuration Editor", closable=True)

        if imgui.begin_tab_bar("ConfigurationEditorTabBar"):
            for method in self.model_and_extra:
                if imgui.begin_tab_item(method).selected:
                    self.draw_tab(method)
                    imgui.end_tab_item()

            imgui.end_tab_bar()

        imgui.end()

    def draw_tab(self, method: str) -> None:
        model, extra = self.model_and_extra[method]

        if imgui.button(f"Populate `{method}` request"):
            JSON_RPC_REQUEST_WINDOW.rpc_kind_n = 0
            JSON_RPC_REQUEST_WINDOW.rpc_method = method

            try:
                JSON_RPC_REQUEST_WINDOW.rpc_params = model.__class__.model_validate(
                    model.model_dump()
                ).model_dump_json(
                    indent=2,
                )
            except Exception as e:
                JSON_RPC_REQUEST_WINDOW.rpc_params = f"Error parsing JSON: {e}"

            imgui.set_window_focus_labeled("JSON RPC Request Window")

        imgui.separator()

        model, extra = self.draw_obj(
            model,
            extra,
            model.__class__.__name__,
            model.__class__,
        )

    def draw_obj(
        self, obj: Any, extra: dict[str, Any], full_name: str, cls: type
    ) -> tuple[Any, dict[str, Any]]:
        """
        obj is what it is, cls is what it should be
        """
        origin, _args = get_origin(cls), get_args(cls)
        name = full_name.split(".")[-1]

        if origin is Union:
            return self.draw_union(obj, extra, full_name, cls)

        # Built-in types
        elif cls is None or cls is NoneType:
            return None, extra
        elif cls is str or cls is Path:
            return imgui.input_text(f"{name}##{full_name}", str(obj), 400)[1], extra
        elif cls is int:
            return imgui.input_int(f"{name}##{full_name}", obj)[1], extra
        elif cls is float:
            return imgui.input_float(f"{name}##{full_name}", obj)[1], extra
        elif cls is bool:
            return imgui.checkbox(f"{name}##{full_name}", obj)[1], extra

        elif origin is dict or cls is dict:
            return self.draw_dict(obj, extra, full_name, cls)
        elif origin is list or cls is list:
            return self.draw_list(obj, extra, full_name, cls)
        elif issubclass(cls, BaseModel):
            return self.draw_base_model(obj, extra, full_name, cls)
        elif issubclass(cls, Enum):
            return self.draw_enum(obj, extra, full_name, cls)
        else:
            imgui.text(f"{full_name}: {cls} (unknown)")
            return obj, extra

    def draw_enum(
        self, obj: Enum | Any, extra: dict[str, Any], full_name: str, cls: type[Enum]
    ) -> tuple[Enum, dict[str, Any]]:
        name = full_name.split(".")[-1]

        ENUM_ITEMS_KEY = f"{full_name}.enum_items"
        ENUM_CURRENT_KEY = f"{full_name}.enum_current"

        if ENUM_ITEMS_KEY not in extra:
            extra[ENUM_ITEMS_KEY] = [item.name for item in cls]
        if ENUM_CURRENT_KEY not in extra:
            extra[ENUM_CURRENT_KEY] = next(
                (i for i, item in enumerate(cls) if item == obj),
                0,
            )

        _, extra[ENUM_CURRENT_KEY] = imgui.combo(
            label=f"{name}##{full_name}",
            current=extra[ENUM_CURRENT_KEY],
            items=extra[ENUM_ITEMS_KEY],
        )

        return cls[extra[ENUM_ITEMS_KEY][extra[ENUM_CURRENT_KEY]]], extra

    def draw_union(
        self, obj: Any, extra: dict[str, Any], full_name: str, cls: type
    ) -> tuple[Any, dict[str, Any]]:
        args = get_args(cls)
        name = full_name.split(".")[-1]

        UNION_ITEMS_KEY = f"{full_name}.union_items"
        UNION_CURRENT_KEY = f"{full_name}.union_current"

        if UNION_ITEMS_KEY not in extra:
            extra[UNION_ITEMS_KEY] = [arg.__name__ for arg in args]
        if UNION_CURRENT_KEY not in extra:
            extra[UNION_CURRENT_KEY] = next(
                (i for i, arg in enumerate(args) if arg == obj.__class__),
                -1,
            )

        _, extra[UNION_CURRENT_KEY] = imgui.combo(
            label=f"{name}'s type##{full_name}",
            current=extra[UNION_CURRENT_KEY],
            items=extra[UNION_ITEMS_KEY],
        )

        return self.draw_obj(
            obj,
            extra,
            full_name,
            args[extra[UNION_CURRENT_KEY]],
        )

    def draw_base_model(
        self,
        obj: BaseModel | Any,
        extra: dict[str, Any],
        full_name: str,
        cls: type[BaseModel],
    ) -> tuple[BaseModel, dict[str, Any]]:
        if not isinstance(obj, cls):
            obj = try_construct_base_model(cls)

        imgui.text(full_name)

        imgui.indent()

        # Why is this necessary?
        if not isinstance(obj.__pydantic_fields_set__, set):
            obj.__pydantic_fields_set__ = set()

        for field_name, field in cls.model_fields.items():
            field_full_name = f"{full_name}.{field_name}"
            if field_full_name not in extra:
                extra[field_full_name] = {}

            result, extra[field_full_name] = self.draw_obj(
                getattr(obj, field_name),
                extra[field_full_name],
                field_full_name,
                field.annotation if field.annotation is not None else NoneType,
            )

            setattr(obj, field_name, result)

        imgui.unindent()

        return obj, extra

    def draw_dict(
        self,
        obj: dict[Any, Any] | Any,
        extra: dict[str, Any],
        full_name: str,
        cls: type[dict[Any, Any]],
    ) -> tuple[dict[Any, Any] | Exception, dict[str, Any]]:
        if not isinstance(obj, dict):
            obj = {}

        name = full_name.split(".")[-1]

        DICT_KEY = f"{full_name}.dict"
        if DICT_KEY not in extra:
            try:
                extra[DICT_KEY] = json.dumps(obj, indent=2)
            except Exception:
                extra[DICT_KEY] = "{}"

        _, extra[DICT_KEY] = imgui.input_text_multiline(
            f"{name}##{full_name}",
            extra[DICT_KEY],
            4096 * 16,
        )

        try:
            return json.loads(extra[DICT_KEY]), extra
        except Exception as e:
            return e, extra

    def draw_list(
        self,
        obj: list[Any] | Any,
        extra: dict[str, Any],
        full_name: str,
        cls: type[list[Any]],
    ) -> tuple[list[Any], dict[str, Any]]:
        args = get_args(cls)
        list_cls = str if len(args) == 0 else args[0]

        if not isinstance(obj, list):
            obj = []

        name = full_name.split(".")[-1]

        LEN_KEY = f"{full_name}.len"
        if LEN_KEY not in extra:
            extra[LEN_KEY] = len(obj)

        _, extra[LEN_KEY] = imgui.input_int(
            f"{name} length##{full_name}", extra[LEN_KEY]
        )

        if extra[LEN_KEY] < 0:
            extra[LEN_KEY] = 0

        if extra[LEN_KEY] > len(obj):
            obj.extend([None for _ in range(extra[LEN_KEY] - len(obj))])
        elif extra[LEN_KEY] < len(obj):
            obj = obj[: extra[LEN_KEY]]

        for i in range(len(obj)):
            ITEM_FULL_NAME_KEY = f"{full_name}.{i}"
            if ITEM_FULL_NAME_KEY not in extra:
                extra[ITEM_FULL_NAME_KEY] = {}

            if not issubclass(list_cls, BaseModel):
                imgui.text(f"{name}.{i}")
                imgui.indent()

            obj[i], extra[ITEM_FULL_NAME_KEY] = self.draw_obj(
                obj[i],
                extra[ITEM_FULL_NAME_KEY],
                ITEM_FULL_NAME_KEY,
                list_cls,
            )

            if not issubclass(list_cls, BaseModel):
                imgui.unindent()

        return obj, extra


class SourceEditor(Drawable):
    def __init__(self) -> None:
        super().__init__()

        self.application_path = "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/example/coolstore"
        self.relative_filename = (
            "/src/main/java/com/redhat/coolstore/service/ShippingService.java"
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
                        # if imgui.selectable("getRAGSolution")[0]:
                        #     JSON_RPC_REQUEST_WINDOW.rpc_kind_n = 0
                        #     JSON_RPC_REQUEST_WINDOW.rpc_method = "getRAGSolution"
                        #     JSON_RPC_REQUEST_WINDOW.rpc_params = json.dumps(
                        #         PostGetIncidentSolutionsForFileParams(
                        #             file_name=str(self.file_path),
                        #             file_contents=self.editor_content,
                        #             application_name="coolstore",
                        #             incidents=[incident],
                        #         ).model_dump(),
                        #         indent=2,
                        #     )

                        #     imgui.set_window_focus_labeled("JSON RPC Request Window")

                        if imgui.selectable("getCodeplanAgentSolution")[0]:
                            send_incident = incident.model_copy(deep=True)
                            send_incident.uri = send_incident.uri.replace(
                                "/opt/input/source/",
                                "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/example/coolstore/",
                            )

                            CONFIGURATION_EDITOR.set_params(
                                "getCodeplanAgentSolution",
                                GetCodeplanAgentSolutionParams(
                                    file_path=self.file_path or Path("/"),
                                    incidents=[send_incident],
                                ),
                            )

                            imgui.set_window_focus_labeled("Configuration Editor")

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
                        # print(f"{SOURCE_EDITOR.relative_filename} != {file_path}")
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
                start_server(["python", str(rpc_script_path)])
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

GIT_VFS_UPDATE_PARAMS: GitVFSUpdateParams | None = None


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
    method_and_params=[
        ("initialize", CONFIG),
        (
            "getCodeplanAgentSolution",
            GetCodeplanAgentSolutionParams(
                file_path=Path(
                    "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/example/coolstore/src/main/java/com/redhat/coolstore/service/ShippingService.java"
                ),
                incidents=[
                    ExtendedIncident(
                        uri="file:///home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/example/coolstore/src/main/java/com/redhat/coolstore/service/ShippingService.java",
                        message='Remote EJBs are not supported in Quarkus, and therefore its use must be removed and replaced with REST functionality. In order to do this:\n 1. Replace the `@Remote` annotation on the class with a `@jakarta.ws.rs.Path("<endpoint>")` annotation. An endpoint must be added to the annotation in place of `<endpoint>` to specify the actual path to the REST service.\n 2. Remove `@Stateless` annotations if present. Given that REST services are stateless by nature, it makes it unnecessary.\n 3. For every public method on the EJB being converted, do the following:\n - In case the method has no input parameters, annotate the method with `@jakarta.ws.rs.GET`; otherwise annotate it with `@jakarta.ws.rs.POST` instead.\n - Annotate the method with `@jakarta.ws.rs.Path("<endpoint>")` and give it a proper endpoint path. As a rule of thumb, the method name can be used as endpoint, for instance:\n ```\n @Path("/increment")\n public void increment() \n ```\n - Add `@jakarta.ws.rs.QueryParam("<param-name>")` to any method parameters if needed, where `<param-name>` is a name for the parameter.',
                        code_snip=" 2  \n 3  import java.math.BigDecimal;\n 4  import java.math.RoundingMode;\n 5  \n 6  import javax.ejb.Remote;\n 7  import javax.ejb.Stateless;\n 8  \n 9  import com.redhat.coolstore.model.ShoppingCart;\n10  \n11  @Stateless\n12  @Remote\n13  public class ShippingService implements ShippingServiceRemote {\n14  \n15      @Override\n16      public double calculateShipping(ShoppingCart sc) {\n17  \n18          if (sc != null) {\n19  \n20              if (sc.getCartItemTotal() >= 0 && sc.getCartItemTotal() < 25) {\n21  \n22                  return 2.99;",
                        line_number=12,
                        variables={
                            "file": "file:///home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/example/coolstore/src/main/java/com/redhat/coolstore/service/ShippingService.java",
                            "kind": "Class",
                            "name": "Stateless",
                            "package": "com.redhat.coolstore.service",
                        },
                        ruleset_name="quarkus/springboot",
                        ruleset_description="This ruleset gives hints to migrate from Springboot devtools to Quarkus",
                        violation_name="remote-ejb-to-quarkus-00000",
                        violation_description="Remote EJBs are not supported in Quarkus",
                        violation_category=Category.MANDATORY,
                        violation_labels=[
                            "konveyor.io/source=java-ee",
                            "konveyor.io/source=jakarta-ee",
                            "konveyor.io/target=quarkus",
                        ],
                    )
                ],
            ),
        ),
        (
            "testRCM",
            TestRCMParams(
                rcm_root=Path(
                    "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/"
                ),
                file_path=Path(
                    "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/test_file.py"
                ),
                new_content="print('Hello, world!')",
            ),
        ),
    ]
)

# CONFIGURATION_EDITOR = ConfigurationEditorOld()

json_rpc_responses: list[dict[str, Any]] = []
rpc_subprocess_stderr_log = []
rpc_subprocess = None

rpc_script_path = Path(os.path.dirname(os.path.realpath(__file__))) / "main.py"
rpc_server: JsonRpcServer | None = None


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

    if rpc_subprocess is not None:
        rpc_subprocess.terminate()
        rpc_subprocess = None
        rpc_subprocess_stderr_log.append("Subprocess terminated.")

    if rpc_server is not None:
        rpc_server.stop()
        rpc_server = None


def submit_json_rpc_request(kind: str, method: str, params: Any) -> None:
    global rpc_server

    try:
        params_dict = json.loads(params)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return

    if rpc_server is None:
        print("RPC server is not running.")
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
    imgui_io.font_global_scale = 1.3
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
