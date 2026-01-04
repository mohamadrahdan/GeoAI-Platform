# Plugin execution engine (sync execution with a clean contract)

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type
from core.plugins.errors import PluginExecutionError
from core.plugins.interface import BasePlugin
from core.plugins.registry import PluginRegistry
from core.logging.logger import Logger


@dataclass
class PluginExecutor:
    registry: PluginRegistry
    logger: Logger
    default_timeout_seconds: float = 10.0

    def _create_instance(self, plugin_cls: Type[BasePlugin]) -> BasePlugin:
        # Plugins can receive config later; for now we pass empty config
        try:
            return plugin_cls(config={})
        except Exception as exc:
            raise PluginExecutionError(f"Failed to initialize plugin '{plugin_cls.__name__}': {exc}") from exc


