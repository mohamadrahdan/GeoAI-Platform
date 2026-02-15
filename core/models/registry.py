from __future__ import annotations
from typing import Dict, List

from core.models.metadata import ModelMetadata

class ModelRegistry:
    """
    In-memory registry for model metadata.
    Responsible for registration and lookup.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, ModelMetadata]] = {}

    def register(self, metadata: ModelMetadata) -> None:
        name = metadata.name
        version = str(metadata.version)

        if name not in self._store:
            self._store[name] = {}

        if version in self._store[name]:
            raise ValueError(f"Model {name}:{version} already registered.")

        self._store[name][version] = metadata

    def get(self, name: str, version: str) -> ModelMetadata:
        try:
            return self._store[name][version]
        except KeyError:
            raise KeyError(f"Model {name}:{version} not found.")

    def list_versions(self, name: str) -> List[str]:
        if name not in self._store:
            return []
        return sorted(self._store[name].keys())
