import os
import pathlib
import sys
from typing import Any

"""
This file exists because we need to define some constants - specifically file
paths - that are used in multiple places in the codebase. There might be a more
robust solution, but for now, this should suffice
"""

PATH_KAI = os.path.dirname(os.path.abspath(__file__))

# pyinstaller sets sys attributes to help determine when program runs in bin
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    PATH_KAI = sys._MEIPASS

PATH_GIT_ROOT = os.path.join(PATH_KAI, "..")

PATH_SOLUTION_SERVER_ROOT = os.path.join(PATH_GIT_ROOT, "kai_solution_server")

PATH_DATA = os.path.join(PATH_SOLUTION_SERVER_ROOT, "data")

PATH_LLM_CACHE = os.path.join(PATH_KAI, "data", "llm_cache")
PATH_BENCHMARKS = os.path.join(PATH_DATA, "benchmarks")
PATH_MISC = os.path.join(PATH_DATA, "misc")
PATH_SQL = os.path.join(PATH_DATA, "sql")
PATH_TEMPLATES = os.path.join(PATH_DATA, "templates")

PATH_LOCAL_REPO = os.path.join(
    PATH_GIT_ROOT, "kai_solution_server/samples/sample_repos"
)

PATH_TESTS = os.path.join(PATH_GIT_ROOT, "tests")
PATH_TEST_DATA = pathlib.Path(os.path.join(PATH_GIT_ROOT, "tests/test_data"))


def __clean_env() -> dict[str, Any]:
    """
    Returns the environment that should be used when calling out to a subprocess
    """
    env: dict[str, Any] = dict(os.environ)  # make a copy of the environment
    lp_key = "LD_LIBRARY_PATH"  # for GNU/Linux and *BSD.
    lp_orig = env.get(lp_key + "_ORIG")
    if lp_orig is not None:
        env[lp_key] = lp_orig  # restore the original, unmodified value
    else:
        # This happens when LD_LIBRARY_PATH was not set.
        # Remove the env var as a last resort:
        env.pop(lp_key, None)
    return env


ENV = __clean_env()
