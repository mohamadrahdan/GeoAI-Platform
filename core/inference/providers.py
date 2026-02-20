from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Tuple
from core.models.base import BaseModel
from core.models.metadata import ModelMetadata
from core.models.registry import ModelRegistry
from abc import ABC, abstractmethod
from core.models.base import BaseModel

class BaseModelProvider(ABC):
    """Returns a concrete model instance for (name, version)."""
    @abstractmethod
    def get(self, model_name: str, version: str) -> BaseModel:
        raise NotImplementedError
    
    # Optional, but useful for tests and local runs
    def register(self, model: BaseModel) -> None:
        raise NotImplementedError("This provider does not support registration.")
    
@dataclass
class InMemoryModelProvider(BaseModelProvider):
    """Simple provider for tests and local experiments.
    It registers model metadata + versions in the registry, and keeps model instances in memory.
    """
    registry: ModelRegistry
    def __post_init__(self) -> None:
        self._models: Dict[Tuple[str, str], BaseModel] = {}
    def register(self, model: BaseModel) -> None:
        meta: ModelMetadata = model.metadata
        name = meta.name
        version_str = str(meta.version)

        # Ensure the model exists in registry
        try:
            self.registry.register_model(meta)
        except ValueError:
            pass

        # Ensure the version exists
        try:
            self.registry.add_version(name, meta.version)
        except ValueError:
            pass

        self._models[(name, version_str)] = model

    def get(self, model_name: str, version: str) -> BaseModel:
        key = (model_name, version)
        if key not in self._models:
            raise ValueError(f"Model instance not available: {model_name}@{version}")
        return self._models[key]
