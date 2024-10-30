import os
import pathlib
import sys

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
# pyinstaller doesn't maintain the same directory structure and we cannot go up a dir
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    PATH_SOLUTION_SERVER_ROOT = os.path.join(PATH_KAI, "kai_solution_server")

PATH_DATA = os.path.join(PATH_SOLUTION_SERVER_ROOT, "data")

PATH_BENCHMARKS = os.path.join(PATH_DATA, "benchmarks")
PATH_MISC = os.path.join(PATH_DATA, "misc")
PATH_SQL = os.path.join(PATH_DATA, "sql")
PATH_TEMPLATES = os.path.join(PATH_DATA, "templates")

PATH_LOCAL_REPO = os.path.join(
    PATH_GIT_ROOT, "kai_solution_server/samples/sample_repos"
)

PATH_TESTS = os.path.join(PATH_GIT_ROOT, "tests")
PATH_TEST_DATA = pathlib.Path(os.path.join(PATH_GIT_ROOT, "tests/test_data"))
