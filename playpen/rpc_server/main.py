import argparse
import logging
import sys
import time
from io import BufferedIOBase, BufferedReader, BufferedWriter
from typing import cast

from playpen.rpc_server.rpc import BareJsonStream, JsonRpcServer
from playpen.rpc_server.server import app

logging.basicConfig()
logging.addLevelName(logging.DEBUG - 5, "TRACE")

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG - 5)


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.description = "Kai RPC Server"


def main() -> None:
    time.sleep(1)
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    _args = parser.parse_args()

    log.info("Starting Kai RPC Server")
    log.log(logging.DEBUG - 5, "Trace log level enabled")

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
