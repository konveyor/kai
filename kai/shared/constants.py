import os
import sys
from pathlib import Path

"""
This file exists because we need to define some constants - specifically file
paths - that are used in multiple places in the codebase. There might be a more
robust solution, but for now, this should suffice
"""


PATH_GIT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)), "..", "..").resolve()

PATH_KAI = PATH_GIT_ROOT / "kai"

# pyinstaller sets sys attributes to help determine when program runs in bin
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    PATH_KAI = Path(sys._MEIPASS)

PATH_SERVER = PATH_KAI / "server"

PATH_DATA = PATH_SERVER / "data"

# TODO: Change benchmarks to tests directory
PATH_BENCHMARKS = PATH_DATA / "benchmarks"
PATH_MISC = PATH_DATA / "misc"
PATH_SQL = PATH_DATA / "sql"
PATH_TEMPLATES = PATH_DATA / "templates"

PATH_SAMPLE_REPOS = PATH_GIT_ROOT / "samples" / "sample_repos"

PATH_TESTS = PATH_GIT_ROOT / "tests"

PATH_TEST_DATA = PATH_TESTS / "test_data"
