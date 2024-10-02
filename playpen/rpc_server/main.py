import argparse
import logging

from playpen.rpc_server.server import KAI_RPC_SERVER

log = logging.getLogger(__name__)


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.description = "Kai RPC Server"


def main() -> None:
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    _args = parser.parse_args()

    log.info("Starting Kai RPC Server")

    KAI_RPC_SERVER.run()
