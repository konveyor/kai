#!/usr/bin/python3

"""This module is intended to facilitate using Konveyor with LLMs."""

import logging
import os
import pprint
from functools import lru_cache

from aiohttp import web
from gunicorn.app.wsgiapp import WSGIApplication

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


@lru_cache
def get_config():
    if not os.path.exists(os.path.join(PATH_KAI, "config.toml")):
        raise FileNotFoundError("Config file not found.")

    return KaiConfig.model_validate_filepath(os.path.join(PATH_KAI, "config.toml"))


def app() -> web.Application:
    config = get_config()

    print(f"Config loaded: {pprint.pformat(config)}")

    initLoggingFromConfig(config)

    webapp = web.Application()
    webapp["kai_application"] = KaiApplication(config)
    webapp["kai_config"] = config
    webapp.add_routes(kai_routes)

    log.info("Kai server is ready to receive requests.")
    return webapp


class StandaloneApplication(WSGIApplication):
    def __init__(self, app_uri, options=None):
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self):
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
