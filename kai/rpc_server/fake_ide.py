"""
A fake IDE client that connects to the Kai RPC Server.
"""

import argparse
import logging
import os
import subprocess  # trunk-ignore(bandit/B404)
import threading
import time
from io import BufferedReader, BufferedWriter
from pathlib import Path
from types import SimpleNamespace
from typing import IO, Any, cast

from kai.jsonrpc.core import JsonRpcServer
from kai.jsonrpc.models import JsonRpcId
from kai.jsonrpc.streams import BareJsonStream
from kai.jsonrpc.util import get_logger
from kai.kai_config import KaiConfigModels
from kai.logging.kai_logging import get_logger
from kai.rpc_server.server import KaiRpcApplication

BLUE = "\033[94m"
RESET = "\033[0m"

log = get_logger("jsonrpc")

rpc_log = get_logger(
    "rpc_subprocess",
    formatter=logging.Formatter(
        fmt="rpc_log: %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ),
)

app = KaiRpcApplication()


@app.add_notify(method="logMessage")
def log_message(
    app: KaiRpcApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
) -> None:
    hack = SimpleNamespace(**params)
    hack.getMessage = lambda: hack.message
    hack.exc_info = None
    hack.exc_text = None
    hack.stack_info = None

    rpc_log.handle(hack)  # type: ignore[arg-type]


def log_stderr(stderr: IO[bytes]) -> None:
    for line in iter(stderr.readline, b""):
        print(f"{BLUE}rpc_err: {line.decode('utf-8')}{RESET}", end="")


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.description = "Fake IDE client using Kai RPC Server"


def main() -> None:
    log.handlers[0].formatter = logging.Formatter(
        fmt=BLUE
        + "ide_log: %(asctime)s - %(name)s - %(levelname)s - %(message)s"
        + RESET,
    )

    rpc_log.info("Starting Fake IDE client using Kai RPC Server")

    parser = argparse.ArgumentParser()
    add_arguments(parser)
    _args = parser.parse_args()

    log.info("Starting Fake IDE client using Kai RPC Server")

    current_directory = Path(os.path.dirname(os.path.realpath(__file__)))
    rpc_binary_path = current_directory / "main.py"
    rpc_subprocess = subprocess.Popen(  # trunk-ignore(bandit/B603,bandit/B607)
        ["python", rpc_binary_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stderr_thread_1 = threading.Thread(target=log_stderr, args=(rpc_subprocess.stderr,))
    stderr_thread_1.start()

    rpc_server = JsonRpcServer(
        json_rpc_stream=BareJsonStream(
            cast(BufferedReader, rpc_subprocess.stdout),
            cast(BufferedWriter, rpc_subprocess.stdin),
        ),
        app=app,
        request_timeout=5.0,
    )
    rpc_server.start()

    log.info("Letting the RPC server start up")
    time.sleep(1)

    try:
        result = rpc_server.send_request(
            "initialize",
            {
                "processId": os.getpid(),
                "rootUri": "file:///path/to/root",
                "kantraUri": "file:///path/to/kantra",
                "modelProvider": KaiConfigModels(
                    provider="fake_provider",
                    args={},
                ),
                "kaiBackendUrl": "http://localhost:8080",
                "logLevel": "TRACE",
                "fileLogLevel": "TRACE",
                "logDirUri": f"{current_directory}/logs",
            },
        )

        print(repr(result))
    except Exception:  # trunk-ignore(bandit/B110)
        pass
    finally:
        rpc_subprocess.terminate()
        rpc_subprocess.wait()
        rpc_server.stop()


if __name__ == "__main__":
    main()
