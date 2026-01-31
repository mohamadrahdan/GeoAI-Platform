from __future__ import annotations

from typing import Protocol, Optional
import logging
from core.config.loader import AppConfig, load_config
from core.logging.logger import get_logger as get_app_logger


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

def get_module_logger(name: str, config: Optional[AppConfig] = None):
    """
    Returns a module-scoped logger.
    Keeps backward compatibility with the app-wide logger factory.
    """
    cfg = config or load_config()
    base_logger = get_app_logger(cfg)
    # If your Logger is a Protocol over std logging, this may be a no-op.
    # You can also just return base_logger if it doesn't support getChild.
    if hasattr(base_logger, "getChild"):
        return base_logger.getChild(name)
    return base_logger