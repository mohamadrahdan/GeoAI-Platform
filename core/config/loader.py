from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from core.config.settings import settings


@dataclass(frozen=True)
class AppConfig:
    env: str
    data_root: Path
    log_level: str


def load_config() -> AppConfig:
    """
    Loads the core application configuration, utilizing the environment-aware
    settings profile from settings.py.
    """
    data_root = Path(settings.DATA_ROOT_RAW).expanduser().resolve()
    data_root.mkdir(parents=True, exist_ok=True)

    return AppConfig(
        env=settings.APP_ENV, data_root=data_root, log_level=settings.LOG_LEVEL
    )


def get_database_url() -> str:
    return settings.DATABASE_URL
