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
    logger.setLevel(logging.INFO)
    return logger
