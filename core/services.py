from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from core.config.loader import AppConfig, load_config
from core.logging.logger import get_logger, Logger

from core.plugins.registry import PluginRegistry
from core.plugins.discovery import discover_plugins

@dataclass
class ServiceContainer:
    """
    A lightweight dependency container for core services.
    - Keeps initialization in one place
    - Makes testing easier (swap services)
    - Avoids circular imports across core/backends
    """

    config: AppConfig
    logger: Logger

    # Placeholders for Phase 2+ components
    data_manager: Optional[object] = None
    plugin_registry: Optional[object] = None
    llm_engin: Optional[object] = None
    
    @classmethod
    def build(cls) -> "ServiceContainer":
        """Build the container with minimal required services(config+logger)"""
        config = load_config()
        logger = get_logger(config)

        registry = PluginRegistry()
        discover_plugins("plugins", registry)

        logger.info("ServiceContainer initialized.")
        logger.info("Plugins discovered: %s", registry.list())
        
        return cls(config=config, 
                   logger=logger,
                   plugin_registry=registry,
                   )
    


# singleton_style accessor 
_container: Optional[ServiceContainer] = None

def get_container() -> ServiceContainer:
    """
    Returns a global singleton container.
    In production you can switch to more advanced DI later.
    """
    global _container
    if _container is None:
        _container = ServiceContainer.build()
    return _container