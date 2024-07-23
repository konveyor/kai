#!/usr/bin/python3

"""This module is intended to facilitate using Konveyor with LLMs."""

import argparse
import logging
import os
import pprint

from aiohttp import web

from kai.constants import PATH_KAI
from kai.kai_logging import initLoggingFromConfig
from kai.models.kai_config import KaiConfig
from kai.routes import kai_routes
from kai.service.kai_application.kai_application import KaiApplication

log = logging.getLogger(__name__)


# TODO: Repo lives both on client and on server. Determine either A) Best way to
# rectify differences or B) Only have the code on one and pass stuff between
# each other
# - can be solved by getting last common commits and then applying a git diff in
#   the same manner as `git stash apply`


def app() -> web.Application:
    if not os.path.exists(os.path.join(PATH_KAI, "config.toml")):
        raise FileNotFoundError("Config file not found.")

    config = KaiConfig.model_validate_filepath(os.path.join(PATH_KAI, "config.toml"))

    if os.getenv("LOG_LEVEL") is not None:
        config.log_level = os.getenv("LOG_LEVEL").upper()
    if os.getenv("DEMO_MODE") is not None:
        config.demo_mode = os.getenv("DEMO_MODE").lower() == "true"
    if os.getenv("TRACE") is not None:
        config.trace_enabled = os.getenv("TRACE").lower() == "true"
    if os.getenv("LOG_DIR") is not None:
        config.log_dir = os.getenv("LOG_DIR")

    print(f"Config loaded: {pprint.pformat(config)}")

    initLoggingFromConfig(config)

    webapp = web.Application()
    webapp["kai_application"] = KaiApplication(config)
    webapp.add_routes(kai_routes)

    return webapp


def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "-log",
        "--loglevel",
        default=os.getenv("LOG_LEVEL", "info"),
        choices=["debug", "info", "warning", "error", "critical"],
        help="""Provide logging level.
Options:
- debug: Detailed information, typically of interest only when diagnosing problems.
- info: Confirmation that things are working as expected.
- warning: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
- error: Due to a more serious problem, the software has not been able to perform some function.
- critical: A serious error, indicating that the program itself may be unable to continue running.
Example: --loglevel debug (default: warning)""",
    )

    arg_parser.add_argument(
        "-demo",
        "--demo_mode",
        default=(os.getenv("DEMO_MODE").lower() == "true"),
        action=argparse.BooleanOptionalAction,
    )

    args, _ = arg_parser.parse_known_args()

    os.environ["LOG_LEVEL"] = str(args.loglevel)
    os.environ["DEMO_MODE"] = str(args.demo_mode).lower()

    web.run_app(app())


if __name__ == "__main__":
    main()
