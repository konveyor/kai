# python-lsp-jsonrpc

import argparse
import json
import logging
import sys
import time

from playpen.rpc_server.server import KaiRpcServer
from playpen.rpc_server.streams import LSPStyleStreamReader, LSPStyleStreamWriter

log = logging.getLogger(__name__)


LOG_FORMAT = "%(asctime)s {0} - %(levelname)s - %(name)s - %(message)s".format(
    time.localtime().tm_zone
)


def configure_logging(level="INFO", log_config=None, log_file=None) -> None:
    root_logger = logging.root

    if log_config:
        with open(log_config, "r") as log_config_file:
            logging.config.dictConfig(json.load(log_config_file))
    else:
        formatter = logging.Formatter(LOG_FORMAT)
        if log_file:
            handler = logging.handlers.RotatingFileHandler(
                log_file,
                mode="a",
                maxBytes=32 * 1024 * 1024,
                backupCount=5,
                encoding=None,
                delay=0,
            )
        else:
            handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

    root_logger.setLevel(level)


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.description = "Kai RPC Server"

    parser.add_argument(
        "--check-parent-process",
        action="store_true",
        help="Check whether parent process is still alive using os.kill(ppid, 0) "
        "and auto shut down language server process when parent process is not alive."
        "Note that this may not work on a Windows machine.",
    )

    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument(
        "--log-config", help="Path to a JSON file containing Python logging config."
    )
    log_group.add_argument(
        "--log-file",
        help="Redirect logs to the given file instead of writing to stderr."
        "Has no effect if used with --log-config.",
    )

    parser.add_argument(
        "--level",
        default="INFO",
        help="Increase verbosity of log output, overrides log config file",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()
    configure_logging(args.level, args.log_config, args.log_file)

    # binary stdio
    stdin, stdout = sys.stdin.buffer, sys.stdout.buffer
    log.info("Starting Kai RPC Server")

    server = KaiRpcServer(
        LSPStyleStreamReader(stdin),
        LSPStyleStreamWriter(stdout),
        args.check_parent_process,
    )
    server.start()


if __name__ == "__main__":
    main()
