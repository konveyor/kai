# TODO: More robust logging
import sys
from typing import Any

log_file = open("stderr.log", "a+")
log_file.close()


def log(*args: Any, **kwargs: Any) -> None:
    print(*args, file=log_file if not log_file.closed else sys.stderr, **kwargs)
