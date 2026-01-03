# Central plugin registry

from __future__ import annotations
from typing import Dict, List, Type
from core.plugins.interface import BasePlugin


class PluginRegistry:
    "In-memory registry for plugins"

    def __init__(self) -> None:
        self._plugins: Dict[str, Type[BasePlugin]] = {}

    def register(self, plugin_cls: Type[BasePlugin]) -> None:
        "Register a plugin class by its unique name"
        name = getattr(plugin_cls, "name", None)
        if not name:
            raise ValueError("Plugin must define a 'name' attribute")
        self._plugins[name] = plugin_cls

    def get(self, name: str) -> Type[BasePlugin]:
        "Retrieve a plugin class by name"
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not registered")
        return self._plugins[name]

    def list(self) -> List[str]:
        "List all registered plugin names"
        return sorted(self._plugins.keys())
