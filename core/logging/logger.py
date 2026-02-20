from __future__ import annotations

import logging
from typing import Optional, Protocol

from core.config.loader import AppConfig, load_config


class Logger(Protocol):
    def info(self, msg: str, *args, **kwargs) -> None: ...
    def warning(self, msg: str, *args, **kwargs) -> None: ...
    def error(self, msg: str, *args, **kwargs) -> None: ...
    def debug(self, msg: str, *args, **kwargs) -> None: ...


def get_logger(config: AppConfig) -> logging.Logger:
    """
    App-level logger factory.
    Configures the 'geoai' logger once and then reuses it.
    """
    logger = logging.getLogger("geoai")
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config.log_level, logging.INFO))

    handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_module_logger(name: str, config: Optional[AppConfig] = None) -> Logger:
    """
    Module-scoped logger helper.
    Avoids circular imports by calling get_logger locally.
    """
    cfg = config or load_config()
    base_logger = get_logger(cfg)

    # std logging supports getChild; if not, return base logger
    if hasattr(base_logger, "getChild"):
        return base_logger.getChild(name)  # type: ignore[attr-defined]
    return base_logger