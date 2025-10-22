import os
import sys
from pathlib import Path
from typing import Any

"""
This file exists because we need to define some constants - specifically file
paths - that are used in multiple places in the codebase. There might be a more
robust solution, but for now, this should suffice.

Note: We sometimes use `os.path.abspath` as opposed to `Path.resolve()` because
the former will resolve relative paths, but not symlinks. This is in line with
what Go does. 
"""

PATH_KAI = Path(os.path.dirname(os.path.abspath(__file__)))

# pyinstaller sets sys attributes to help determine when program runs in bin
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    PATH_KAI = Path(sys._MEIPASS)

PATH_GIT_ROOT = Path(os.path.abspath(os.path.join(PATH_KAI, "..")))

PATH_SOLUTION_SERVER_ROOT = PATH_GIT_ROOT / "kai_solution_server"

PATH_DATA = PATH_SOLUTION_SERVER_ROOT / "data"

PATH_LLM_CACHE = PATH_KAI / "data" / "llm_cache"
PATH_BENCHMARKS = PATH_DATA / "benchmarks"
PATH_MISC = PATH_DATA / "misc"
PATH_SQL = PATH_DATA / "sql"
PATH_TEMPLATES = PATH_DATA / "templates"

PATH_LOCAL_REPO = PATH_GIT_ROOT / "kai_solution_server" / "samples" / "sample_repos"

PATH_TESTS = PATH_GIT_ROOT / "tests"
PATH_TEST_DATA = PATH_GIT_ROOT / "tests" / "test_data"


def __clean_env() -> dict[str, Any]:
    """
    Returns the environment that should be used when calling out to a subprocess
    """
    if not getattr(sys, "frozen", False) or not hasattr(sys, "_MEIPASS"):
        return dict(os.environ)

    env: dict[str, Any] = dict(os.environ)  # make a copy of the environment
    # fix for windows in common pitfalls
    # https://pyinstaller.org/en/stable/common-issues-and-pitfalls.html#windows
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.kernel32.SetDllDirectoryW(None)
        return env

    # fix for mac os in common pitfalls
    # https://pyinstaller.org/en/stable/common-issues-and-pitfalls.html#macos
    if sys.platform == "darwin":
        for key, path in os.environ.items():
            if sys._MEIPASS in path:
                env.pop(key)

        return env

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
