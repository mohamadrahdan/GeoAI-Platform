from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from core.config.loader import AppConfig, load_config
from core.logging.logger import get_logger, Logger
from core.plugins.registry import PluginRegistry
from core.plugins.discovery import discover_plugins
from core.data_manager.local_fs import LocalFileSystemDataManager
from core.data_manager.cache import SimpleCache
from core.data_manager.base import BaseDataManager
from core.llm.engine import BaseLLMEngine, NullLLMEngine
from core.models.registry import ModelRegistry
from core.models.artifacts import LocalArtifactStore

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
    data_manager: BaseDataManager
    cache: SimpleCache
    #llm_engin: Optional[object] = None
    llm_engine: BaseLLMEngine
    registry: ModelRegistry  # model registry
    plugin_registry: Optional[PluginRegistry] = None
    

    @classmethod
    def build(cls) -> "ServiceContainer":
        config = load_config()
        logger = get_logger(config) 
        llm_engine = NullLLMEngine()
        # Plugin registry (rename to avoid confusion)
        plugin_registry = PluginRegistry()
        discover_plugins("plugins", plugin_registry)

        data_manager = LocalFileSystemDataManager(config.data_root)
        cache = SimpleCache()

        # Model registry
        artifact_store = LocalArtifactStore(root_dir=Path("artifacts"))
        model_registry = ModelRegistry(artifact_store=artifact_store)

        logger.info("ServiceContainer initialized.")
        logger.info("Plugins discovered: %s", plugin_registry.list())
        logger.info("DataManager initialized at %s", config.data_root)

        return cls(
            config=config,
            logger=logger,
            plugin_registry=plugin_registry,
            data_manager=data_manager,
            cache=cache,
            llm_engine=llm_engine,
            registry=model_registry,
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

