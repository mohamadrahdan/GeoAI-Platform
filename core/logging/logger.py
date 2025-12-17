from __future__ import annotations

from typing import Protocol
import logging
from core.config.loader import AppConfig


class Logger(Protocol):
    def info(self, msg: str, *args, **kwargs) -> None: ...
    def warning(self, msg: str, *args, **kwargs) -> None: ...
    def error(self, msg: str, *args, **kwargs) -> None: ...
    def debug(self, msg: str, *args, **kwargs) -> None: ...


def get_logger(config: AppConfig) -> logging.Logger:
    logger = logging.getLogger("geoai")
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config.log_level, logging.INFO))

    handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
