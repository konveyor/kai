#!/usr/bin/python3

"""This module is intended to facilitate using Konveyor with LLMs."""

import argparse
import logging
import pprint
from functools import cache
from typing import Any

from aiohttp import web
from gunicorn.app.wsgiapp import WSGIApplication  # type: ignore[import-untyped]

from kai.kai_config import KaiConfig
from kai.logging.kai_logging import init_logging_from_config
from kai_solution_server.routes import kai_routes
from kai_solution_server.service.incident_store.incident_store import IncidentStore

log = logging.getLogger(__name__)


@cache
def get_config() -> KaiConfig:
    """
    Get the configuration for the server and parse command line arguments.

    Note that this function is cached, so it will only be called once. We do
    this because each gunicorn worker will call this function, and global state
    can get tricky.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config_filepath",
        help="Path to an optional config file.",
        type=str,
        default=None,
        required=False,
    )
    args = parser.parse_args()

    if args.config_filepath:
        return KaiConfig.model_validate_filepath(args.config_filepath)

    return KaiConfig()


def app() -> web.Application:
    config = get_config()

    print(f"Config loaded: {pprint.pformat(config)}")

    init_logging_from_config(config)

    webapp = web.Application()

    webapp["kai_incident_store"] = IncidentStore.incident_store_from_config(config)
    webapp["kai_config"] = config
    webapp.add_routes(kai_routes)

    log.info("Kai server is ready to receive requests.")
    return webapp


class StandaloneApplication(WSGIApplication):  # type: ignore[misc]
    """
    This class is used to run the aiohttp app with gunicorn. While we could use
    the `gunicorn` command, this class allows us to call `server.py` directly.
    """

    def __init__(self, app_uri: str, options: dict[str, Any] | None = None) -> None:
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


if __name__ == "__main__":
    config = get_config()

    options = {
        "timeout": config.gunicorn_timeout,
        "workers": config.gunicorn_workers,
        "bind": config.gunicorn_bind,
        "worker_class": "aiohttp.GunicornWebWorker",
    }

    StandaloneApplication("kai.server:app()", options).run()
