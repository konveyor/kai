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

from playpen.client.cli import (
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

from kai.logging.logging import parent_log, setup_file_handler
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
            except Exception as e:
                self.send_response(
                    rpc_id, None, ResponseError(ErrorCodes.InternalError, str(e))
                )


class CustomRpcEndpoint(JsonRpcEndpoint):
    def __add_header(self, json_string: str):
        return JSON_RPC_REQ_FORMAT.format(
            json_string_len=len(json_string), json_string=json_string
        )

    def send_request(self, message):
        json_string = json.dumps(message, cls=MyEncoder)
        jsonrpc_req = self.__add_header(json_string)
        print(f"sending data over stdin {repr(jsonrpc_req)}")
        with self.write_lock:
            self.stdin.buffer.write(jsonrpc_req.encode())
            self.stdin.flush()

    def recv_response(self):
        with self.read_lock:
            message_size = None
            while True:
                line = self.stdout.buffer.readline().decode("utf-8")
                if not line:
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

            jsonrpc_res = self.stdout.buffer.read(message_size).decode("utf-8")
            print(f"read data from stdout {repr(jsonrpc_res)}")
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
        log.debug(f"got rpc params {rpc_params._data}")
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
            result = generate_fix(
                trace,
                config,
                rpc_params.app_name,
                "java",
                rpc_params.input_file_path,
                prompt,
                model_provider,
            )
            return result.updated_file
        except Exception as e:
            trace.exception(-1, -1, e, traceback.format_exc())
            log.debug(f"failed to generate fix: {e}")
            raise ResponseError(
                ErrorCodes.InternalError, f"failed to generate fix - {str(e)}"
            ) from e
        finally:
            end = time.time()
            trace.end(end)
            log.info(
                f"END - completed in '{end-start}s:  - App: '{rpc_params.app_name}', File: '{rpc_params.input_file_path}' with {len(incidents)} incidents'"
            )


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
