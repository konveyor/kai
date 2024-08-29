#!/usr/bin/python3

"""This module is intended to facilitate using Konveyor with LLMs."""

import json
import logging
import os
import sys
import time
import traceback
from typing import Any, Dict, List
from warnings import filterwarnings

from cli import (
    generate_fix,
    get_config,
    get_impacted_files_from_report,
    get_model_provider,
    get_trace,
    render_prompt,
)
from pylspclient.json_rpc_endpoint import JsonRpcEndpoint, MyEncoder
from pylspclient.lsp_client import LspEndpoint as RpcServer
from pylspclient.lsp_errors import ErrorCodes, ResponseError

from kai.kai_logging import parent_log, setup_file_handler
from kai.models.report_types import ExtendedIncident

log = logging.getLogger("kai-rpc")

JSON_RPC_REQ_FORMAT = "Content-Length: {json_string_len}\r\n\r\n{json_string}"
LEN_HEADER = "Content-Length: "
TYPE_HEADER = "Content-Type: "


class CustomRpcServer(RpcServer):
    def run(self):
        while not self.shutdown_flag:
            try:
                jsonrpc_message = self.json_rpc_endpoint.recv_response()
                if jsonrpc_message is None:
                    log.debug("server quit")
                    break
                method = jsonrpc_message.get("method")
                result = jsonrpc_message.get("result")
                error = jsonrpc_message.get("error")
                rpc_id = jsonrpc_message.get("id")
                params = jsonrpc_message.get("params")

                if method:
                    if rpc_id is not None:
                        # a call for method
                        if method not in self.method_callbacks:
                            raise ResponseError(
                                ErrorCodes.MethodNotFound,
                                "Method not found: {method}".format(method=method),
                            )
                        result = self.method_callbacks[method](**params["kwargs"])
                        self.send_response(rpc_id, result, None)
                    else:
                        if method not in self.notify_callbacks:
                            log.debug(
                                "Notify method not found: {method}.".format(
                                    method=method
                                )
                            )
                        else:
                            self.notify_callbacks[method](params)
                else:
                    self.handle_result(rpc_id, result, error)
            except ResponseError as e:
                self.send_response(rpc_id, None, e)


class CustomRpcEndpoint(JsonRpcEndpoint):
    def __add_header(self, json_string: str):
        return JSON_RPC_REQ_FORMAT.format(
            json_string_len=len(json_string), json_string=json_string
        )

    def send_request(self, message):
        json_string = json.dumps(message, cls=MyEncoder)
        jsonrpc_req = self.__add_header(json_string)
        log.debug(f"sending res {jsonrpc_req}")
        with self.write_lock:
            self.stdin.write(jsonrpc_req)
            self.stdin.flush()

    def recv_response(self):
        with self.read_lock:
            message_size = None
            while True:
                log.debug("waiting")
                line = self.stdout.readline()
                log.debug("read line")
                log.debug(line)
                if not line:
                    log.debug("empty line")
                    return None
                if not line.endswith("\r\n") and not line.endswith("\n"):
                    raise ResponseError(
                        ErrorCodes.ParseError, "Bad header: missing newline"
                    )
                line = line[: -2 if line.endswith("\r\n") else -1]
                if line == "":
                    break
                elif line.startswith(LEN_HEADER):
                    line = line[len(LEN_HEADER) :]
                    if not line.isdigit():
                        raise ResponseError(
                            ErrorCodes.ParseError, "Bad header: size is not int"
                        )
                    message_size = int(line)
                elif line.startswith(TYPE_HEADER):
                    pass
                else:
                    raise ResponseError(
                        ErrorCodes.ParseError, "Bad header: unkown header"
                    )
            if not message_size:
                raise ResponseError(ErrorCodes.ParseError, "Bad header: missing size")

            log.debug(f"waiting to read message of size {message_size}")
            jsonrpc_res = self.stdout.read(message_size)
            log.debug(f"read message {jsonrpc_res}")
            return json.loads(jsonrpc_res)


class RPCParams:
    def __init__(self, **kwargs):
        self._data = kwargs

    def json(self):
        return json.dumps(self._data)

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

    @data.setter
    def data(self, data) -> Dict[str, Any]:
        self._data = data

    @property
    def app_name(self) -> str:
        return self._data.get("app_name")

    @app_name.setter
    def app_name(self, name: str):
        self._data["app_name"] = name

    @property
    def config_path(self) -> str:
        return self._data.get("config_path")

    @config_path.setter
    def config_path(self, path: str):
        self._validate_path(path)
        self._data["config_path"] = path

    @property
    def input_file_path(self) -> str:
        return self._data.get("input_file_path")

    @input_file_path.setter
    def input_file_path(self, path: str) -> str:
        self._validate_path(path)
        self._data["input_file_path"] = path

    @property
    def incidents(self) -> List[ExtendedIncident]:
        return self._data.get("incidents", [])

    @incidents.setter
    def incidents(self, incidents: List[ExtendedIncident]):
        self._data["incidents"] = incidents

    @property
    def report_path(self) -> str:
        return self._data.get("report_path", [])

    @report_path.setter
    def report_path(self, path: str):
        self._validate_path(path)
        self._data["report_path"] = path

    @property
    def log_level(self) -> str:
        return self._data.get("log_level", "INFO")

    @log_level.setter
    def log_level(self, level: str):
        self._data["log_level"] = level

    def _validate_path(self, path: str, dir: bool = False) -> bool:
        if not os.path.exists(path):
            raise ResponseError(
                ErrorCodes.InvalidParams,
                f"path {path} does not exist",
            )
        if dir and not os.path.isdir(path):
            raise ResponseError(
                ErrorCodes.InvalidParams, f"file path is not a directory {path}"
            )
        if not dir and os.path.isdir(path):
            raise ResponseError(
                ErrorCodes.InvalidParams, f"file path is a directory {path}"
            )


class KaiClientRPCServer:
    def get_incident_solutions_for_file(self, **kwargs) -> str:
        rpc_params = RPCParams(**kwargs)
        log.debug(f"got rpc params {rpc_params}")
        config = get_config(rpc_params.config_path)

        setup_file_handler(
            parent_log,
            "kai_server.log",
            config.log_dir,
            rpc_params.log_level,
            silent=True,
        )

        model_provider = get_model_provider(config.models)

        incidents = []
        if rpc_params.incidents:
            incidents = json.loads(rpc_params.incidents)
        elif rpc_params.report_path:
            impacted_files = get_impacted_files_from_report(rpc_params.report_path)
            for k, v in impacted_files.items():
                if rpc_params.input_file_path.endswith(k):
                    incidents = v
                    break
            else:
                raise ResponseError(ErrorCodes.RequestCancelled, "no incidents to fix")
        else:
            raise ResponseError(
                ErrorCodes.InvalidParams,
                "either params.incidents or params.report_path is required",
            )

        file_contents = ""
        with open(rpc_params.input_file_path, "r") as f:
            file_contents = f.read()

        start = time.time()
        try:
            trace = get_trace(
                config,
                model_provider,
                "single",
                rpc_params.app_name,
                os.path.basename(rpc_params.input_file_path),
            )
            trace.start(start)
            prompt = render_prompt(
                trace,
                os.path.basename(rpc_params.input_file_path),
                "java",
                file_contents,
                incidents,
                model_provider,
            )
            log.debug("making llm request to generate a fix")
            result = generate_fix(
                trace,
                config,
                rpc_params.app_name,
                "java",
                rpc_params.input_file_path,
                prompt,
                model_provider,
                use_vcr=False,
            )
            return result.updated_file
        except Exception as e:
            trace.exception(-1, -1, e, traceback.format_exc())
            log.debug(f"error processing file: {e}")
        finally:
            end = time.time()
            trace.end(end)
            log.info(
                f"END - completed in '{end-start}s:  - App: '{rpc_params.app_name}', File: '{rpc_params.input_file_path}' with {len(incidents)} incidents'"
            )

        raise ResponseError("failed to generate fix")


def run_rpc_server():
    # filter warnings so stdout is not polluted
    filterwarnings("ignore", category=RuntimeWarning)
    filterwarnings("ignore", category=DeprecationWarning)
    file_handler = logging.FileHandler("server.log")
    formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(name)s - [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s"
    )
    file_handler.setFormatter(formatter)
    log.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    kai = KaiClientRPCServer()
    # the library gives us a client, we use it as a LSP server by switching stdin / stdout
    CustomRpcServer(
        json_rpc_endpoint=CustomRpcEndpoint(sys.stdout, sys.stdin),
        method_callbacks={
            "get_incident_solutions_for_file": kai.get_incident_solutions_for_file,
        },
        timeout=60,
    ).run()


if __name__ == "__main__":
    try:
        run_rpc_server()
    except Exception as e:
        log.error(f"{traceback.format_exc()}")
        log.error(f"failed running the server {e}")


# class RPC(jsonrpyc.RPC):
#     def _handle_request(self, req: Dict[str, Any]) -> None:
#         log.debug(f"handling request {req}")
#         return super()._handle_request(req)

#     def __init__(self,
#         target: Any | None = None,
#         stdin: jsonrpyc.InputStream | None = None,
#         stdout: jsonrpyc.OutputStream | None = None,
#         *,
#         watch: bool = True,
#         watch_kwargs: dict[str, Any] | None = None):
#         # the wrapped target object
#         self.target = target

#         # open input stream
#         if stdin is None:
#             stdin = sys.stdin
#         self.original_stdin = stdin
#         self.stdin = io.open(stdin.fileno(), "rb")

#         # open output stream
#         if stdout is None:
#             stdout = sys.stdout
#         self.original_stdout = stdout
#         self.stdout = io.open(stdout.fileno(), "wb")

#         # other attributes
#         self._i = -1
#         self._callbacks: dict[int, jsonrpyc.Callback] = {}
#         self._results: dict[int, Any] = {}

#         # create and optionall start the watchdog
#         watch_kwargs = watch_kwargs or {}
#         watch_kwargs["start"] = watch
#         watch_kwargs.setdefault("daemon", target is None)
#         self.watchdog = WatchDog(self, **watch_kwargs)

# class WatchDog(jsonrpyc.Watchdog):
#     def run(self) -> None:
#         """
#         The main run loop of the watchdog thread. Reads the input stream of the :py:class:`RPC`
#         instance and dispatches incoming content to it.

#         :return: None.
#         """
#         log.debug("started thread")
#         log.debug(f"is_stop_set() {self._stop.is_set()}")
#         # reset the stop event
#         self._stop.clear()

#         # stop here when stdin is not set or closed
#         if self.rpc.stdin is None or self.rpc.stdin.closed:
#             return

#         # read new incoming lines
#         last_pos = 0
#         while not self._stop.is_set():
#             lines = None

#             # stop when stdin is closed
#             if self.rpc.stdin.closed:
#                 log.debug("stdin closed")
#                 break

#             if self.rpc.original_stdin and self.rpc.original_stdin.closed:  # type: ignore[attr-defined] # noqa
#                 log.debug("original stdin closed")
#                 break

#             try:
#                 lines = [self.rpc.stdin.readline()]
#             except IOError:
#                 pass

#             if lines:
#                 for b_line in lines:
#                     line = b_line.decode("utf-8").strip()
#                     if line:
#                         self.rpc._handle(line)
#             else:
#                 self._stop.wait(self.interval)
# message_size = None
# line = self.rpc.stdin.readline()
# if not line:
#     break
# line = line.decode("utf-8")
# if not line.endswith("\r\n"):
#     raise jsonrpyc.RPCInvalidRequest("invalid request header, separator not found")
# line = line[:-2]
# if line == "":
#     break
# elif line.startswith(LEN_HEADER):
#     line = line[len(LEN_HEADER):]
#     if not line.isdigit():
#         raise jsonrpyc.RPCInvalidRequest("invalid request header, content-length not found")
#     message_size = int(line)
# elif line.startswith(TYPE_HEADER):
#     pass
# else:
#     raise jsonrpyc.RPCInvalidRequest("invalid request header, unknown header")

# if not message_size:
#     raise jsonrpyc.RPCInvalidRequest("content-length header could not be parsed")

# log.debug(f"data size {message_size}")
# data = self.rpc.stdin.read(message_size+2).decode("utf-8")
# log.debug(f"read data {data}")

# if data:
#     try:
#         self.rpc._handle(data)
#     except json.JSONDecodeError as e:
#         raise jsonrpyc.RPCInvalidRequest(f"invalid request format {e}")
# else:
#     self._stop.wait(self.interval)
