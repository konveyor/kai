import argparse
import sys
from io import BufferedReader, BufferedWriter
from typing import cast

from kai.jsonrpc.core import JsonRpcServer
from kai.jsonrpc.streams import BareJsonStream
from kai.jsonrpc.util import TRACE, get_logger
from kai.rpc_server.server import app

log = get_logger("jsonrpc")


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.description = "Kai RPC Server"


def main() -> None:
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    _args = parser.parse_args()

    log.setLevel(TRACE)
    log.info("Starting Kai RPC Server")
    log.log(TRACE, "Trace log level enabled")

    # mypy incorrectly type checks sys.stdin.buffer and sys.stdout.buffer as
    # simply IO[bytes], rather than as BufferedReader and BufferedWriter for
    # some reason, at least on my machine.
    rpc_server = JsonRpcServer(
        json_rpc_stream=BareJsonStream(
            cast(BufferedReader, sys.stdin.buffer),
            cast(BufferedWriter, sys.stdout.buffer),
        ),
        app=app,
    )

    rpc_server.start()


if __name__ == "__main__":
    main()
