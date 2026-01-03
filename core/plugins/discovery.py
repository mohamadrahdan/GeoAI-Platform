# Automatic plugin discovery

from __future__ import annotations
import importlib
import pkgutil
from typing import Type
from core.plugins.interface import BasePlugin
from core.plugins.registry import PluginRegistry


def discover_plugins(package: str, registry: PluginRegistry) -> None:
    "Discover and register plugins from a given package"
    module = importlib.import_module(package)

    for _, module_name, _ in pkgutil.iter_modules(module.__path__):
        full_module_name = f"{package}.{module_name}.plugin"
        try:
            imported = importlib.import_module(full_module_name)
        except ModuleNotFoundError:
            continue

        for attribute in vars(imported).values():
            if (
                isinstance(attribute, type)
                and issubclass(attribute, BasePlugin)
                and attribute is not BasePlugin
            ):
                registry.register(attribute)
