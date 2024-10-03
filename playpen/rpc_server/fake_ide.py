"""
A fake IDE client that connects to the Kai RPC Server.
"""

import argparse
import logging
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import IO, cast

from kai.models.kai_config import KaiConfigModels
from playpen.rpc_server.rpc import BareJsonStream, JsonRpcServer
from playpen.rpc_server.server import KaiRpcApplication

# Add a formatter to the root logger
formatter = logging.Formatter("\033[94m%(levelname)s:%(name)s:%(message)s\033[0m")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

logging.addLevelName(logging.DEBUG - 5, "TRACE")

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG - 5)

app = KaiRpcApplication()


@app.add_notify(method="logMessage")
def log_message(app: KaiRpcApplication, message: str, level: str):
    print(f"{level}: {message}")


def log_stderr(stderr: IO[bytes], color: str) -> None:
    print("Logging stderr")
    for line in iter(stderr.readline, b""):
        print(f"  {color}{line.decode('utf-8')}\033[0m", end="")


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.description = "Fake IDE client using Kai RPC Server"


def main() -> None:
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    _args = parser.parse_args()

    log.info("Starting Fake IDE client using Kai RPC Server")

    current_directory = Path(os.path.dirname(os.path.realpath(__file__)))
    rpc_binary_path = current_directory / "main.py"
    rpc_subprocess = subprocess.Popen(
        ["python", rpc_binary_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stderr_thread_1 = threading.Thread(
        target=log_stderr, args=(rpc_subprocess.stderr, "\033[91m")
    )
    stderr_thread_1.start()

    import inspect

    log.info(inspect.getmro(rpc_subprocess.stdout.__class__))
    log.info(inspect.getmro(rpc_subprocess.stdin.__class__))

    rpc_server = JsonRpcServer(
        json_rpc_stream=BareJsonStream(
            rpc_subprocess.stdout,
            rpc_subprocess.stdin,
        ),
        app=app,
        request_timeout=5.0,
    )
    rpc_server.start()

    time.sleep(4)

    try:
        result = rpc_server.send_request(
            "initialize",
            processId=os.getpid(),
            rootUri="file:///path/to/root",
            kantraUri="file:///path/to/kantra",
            modelProvider=KaiConfigModels(
                provider="fake_provider",
                args={},
            ),
            kaiBackendUrl="http://localhost:8080",
            logLevel="TRACE",
            fileLogLevel="TRACE",
            logDirUri=f"{current_directory}/logs",
        )

        print(repr(result))
    except Exception:
        pass
    finally:
        rpc_subprocess.terminate()
        rpc_subprocess.wait()
        rpc_server.stop()


if __name__ == "__main__":
    main()
