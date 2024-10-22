import os
from typing import Optional


def str_to_bool(val: str) -> bool:
    """
    Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))


def get_env_bool(key: str, default: Optional[bool] = None) -> bool | None:
    """
    Get a boolean value from an environment variable, returning the default if
    the variable is not set.
    """
    val = os.getenv(key)
    if val is None:
        return default
    return str_to_bool(val)
