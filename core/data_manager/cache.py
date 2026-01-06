from __future__ import annotations

from typing import Any, Dict

class SimpleCache:
    "Minimal in-memory cache (MVP)"

    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    def get(self, key: str) -> Any | None:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def clear(self) -> None:
        self._store.clear()
