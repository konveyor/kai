import argparse
import logging
import sys

from playpen.rpc_server.rpc import JsonRpcServer, LspStyleStream
from playpen.rpc_server.server import app

log = logging.getLogger(__name__)


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.description = "Kai RPC Server"


def main() -> None:
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    _args = parser.parse_args()

    log.setLevel(logging.INFO)  # Set initial log level
    log.info("Starting Kai RPC Server")

    rpc_server = JsonRpcServer(
        json_rpc_stream=LspStyleStream(sys.stdin.buffer, sys.stdout.buffer),
        app=app,
    )

    rpc_server.run()


if __name__ == "__main__":
    main()
