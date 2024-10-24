import argparse
import logging as core_logging
import sys
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import cast

import kai.logging.logging as logging
from kai.jsonrpc.core import JsonRpcServer
from kai.jsonrpc.streams import BareJsonStream
from kai.kai_config import KaiConfig
from kai.rpc_server.server import app

DEFAULT_FORMATTER = core_logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.description = "Kai RPC Server"
    parser.add_argument(
        "-c",
        "--config",
        help="This is the configuration file for the kai rpc server.",
        type=Path,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    _args = parser.parse_args()

    if _args.config:
        config = KaiConfig.model_validate_filepath(_args.config)
        logging.init_logging_from_config(config)

    if logging.log:
        logging.log.info("Starting Kai RPC Server")
    else:
        raise Exception("no logger was configured")

    stderr_handler = core_logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.log.level)
    stderr_handler.setFormatter(DEFAULT_FORMATTER)
    logging.log.addHandler(stderr_handler)

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
