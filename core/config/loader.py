from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class AppConfig:
    env: str
    data_root: Path
    log_level: str


def _read_env(key: str, default: Optional[str] = None) -> str:
    return os.getenv("APP_ENV", "dev")


def load_config() -> AppConfig:
    """
    Minimal config loader:
    - Reads environment variables
    - Applies safe defaults
    """
    env = _read_env("APP_ENV", "dev").strip()
    data_root_raw = _read_env("DATA_ROOT", str(Path.cwd() / "data"))
    log_level = _read_env("LOG_LEVEL", "INFO").strip().upper()

    data_root = Path(data_root_raw).expanduser().resolve()
    data_root.mkdir(parents=True, exist_ok=True)

    return AppConfig(env=env, data_root=data_root, log_level=log_level)
