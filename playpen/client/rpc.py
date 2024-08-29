#!/usr/bin/python3

"""This module is intended to facilitate using Konveyor with LLMs."""

import argparse
import json
import logging
import os
import subprocess
import time
import traceback
from typing import Any, Dict, List, Tuple
from warnings import filterwarnings

import jsonrpyc
from cli import (
    generate_fix,
    get_config,
    get_impacted_files_from_report,
    get_model_provider,
    get_trace,
    render_prompt,
)

from kai.kai_logging import parent_log, setup_file_handler
from kai.models.report_types import ExtendedIncident

log = logging.getLogger("kai-rpc")


class RPCParams:
    def __init__(self, data="{}"):
        self._data = json.loads(data)

    def json(self):
        return json.dumps(self._data)

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

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
            raise jsonrpyc.RPCInvalidParams(f"file path does not exist {path}")
        if dir and not os.path.isdir(path):
            raise jsonrpyc.RPCInvalidParams(f"file path is not a directory {path}")
        if not dir and os.path.isdir(path):
            raise jsonrpyc.RPCInvalidParams(f"file path is a directory {path}")


class KaiClientRPCServer:
    def get_incident_solutions_for_file(self, params: str) -> str:
        rpc_params = RPCParams(params)
        log.debug(f"got rpc params {rpc_params.json()}")

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
                raise jsonrpyc.RPCInvalidRequest("no incidents to fix")
        else:
            raise jsonrpyc.RPCInvalidRequest(
                "either params.incidents or params.report_path is required"
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

        raise jsonrpyc.RPCServerError("failed to generate fix")


def run_rpc_server():
    # filter warnings so stdout is not polluted
    filterwarnings("ignore", category=RuntimeWarning)
    filterwarnings("ignore", category=DeprecationWarning)
    file_handler = logging.FileHandler("server.log")
    formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(name)s - [%(filename)20s:%(lineno)-4s - %(funcName)20s()] - %(message)s"
    )
    file_handler.setFormatter(formatter)
    log.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    jsonrpyc.RPC(KaiClientRPCServer())


if __name__ == "__main__":
    run_rpc_server()
