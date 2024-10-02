"""
A fake IDE client that connects to the Kai RPC Server.
"""

import argparse
import logging
import os
import subprocess
from pathlib import Path
from typing import IO, cast

from kai.models.kai_config import KaiConfigModels
from playpen.rpc_server.rpc import JsonRpcServer, LspStyleStream
from playpen.rpc_server.server import KaiRpcApplication

log = logging.getLogger(__name__)

app = KaiRpcApplication()


@app.add_notify(method="logMessage")
def log_message(app: KaiRpcApplication, message: str, level: str):
    print(f"{level}: {message}")


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.description = "Fake IDE client using Kai RPC Server"


def main() -> None:
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    _args = parser.parse_args()

    print("Starting Fake IDE client using Kai RPC Server")

    current_directory = Path(os.path.dirname(os.path.realpath(__file__)))
    rpc_binary_path = current_directory / "main.py"
    rpc_subprocess = subprocess.Popen(
        ["python", rpc_binary_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    rpc_server = JsonRpcServer(
        json_rpc_stream=LspStyleStream(
            cast(IO[bytes], rpc_subprocess.stdout),
            cast(IO[bytes], rpc_subprocess.stdin),
        ),
        app=app,
        request_timeout=2.0,
    )
    rpc_server.start()

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
            logLevel="DEBUG",
            fileLogLevel="DEBUG",
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
