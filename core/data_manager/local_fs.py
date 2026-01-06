from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.data_manager.base import BaseDataManager

class LocalFileSystemDataManager(BaseDataManager):
    "Local filesystem-based data manager (MVP)"

    def __init__(self, data_root: Path) -> None:
        self.data_root = data_root
        self.data_root.mkdir(parents=True, exist_ok=True)

    def resolve(self, relative_path: str) -> Path:
        return (self.data_root / relative_path).resolve()

    def exists(self, relative_path: str) -> bool:
        return self.resolve(relative_path).exists()

    def load(self, relative_path: str) -> Any:
        path = self.resolve(relative_path)
        if path.suffix.lower() == ".json":
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        # fallback: raw bytes
        return path.read_bytes()

    def save(self, relative_path: str, data: Any) -> None:
        path = self.resolve(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(data, (dict, list)):
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        elif isinstance(data, (bytes, bytearray)):
            path.write_bytes(data)
        else:
            # simple text fallback
            path.write_text(str(data), encoding="utf-8")
