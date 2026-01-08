from __future__ import annotations
from pathlib import Path
from core.common.exceptions import DataAccessError


def safe_resolve(base: Path, relative: str) -> Path:
    """
    Safely resolve a relative path within a base directory.
    Prevents path traversal attacks.
    """
    resolved = (base / relative).resolve()
    if not str(resolved).startswith(str(base.resolve())):
        raise DataAccessError(f"Invalid path access attempt: {relative}")
    return resolved
