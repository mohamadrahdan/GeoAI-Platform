from __future__ import annotations

from typing import Any
import time


def now_ts() -> float:
    "Return current timestamp."
    return time.time()


def ensure_dict(value: Any) -> dict:
    "Ensure value is a dictionary."
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise TypeError("Expected a dict")
    return value
