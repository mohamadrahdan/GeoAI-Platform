from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple
from core.models.metadata import ModelMetadata, ModelVersion
from core.models.artifacts import ArtifactRef, ArtifactStore 

@dataclass
class RegisteredModel:
    metadata: ModelMetadata
    versions: Dict[str, ModelVersion]
    artifacts: Dict[Tuple[str, str], ArtifactRef]  # key: (version, filename) 

class ModelRegistry:
    def __init__(self, artifact_store: ArtifactStore) -> None:
        self._artifact_store = artifact_store
        self._models: Dict[str, RegisteredModel] = {}

    def register_model(self, metadata: ModelMetadata) -> None:
        if metadata.name in self._models:
            raise ValueError(f"Model already registered: {metadata.name}")
        self._models[metadata.name] = RegisteredModel(
            metadata=metadata,
            versions={},
            artifacts={},
        )

    def add_version(self, model_name: str, version: ModelVersion) -> None:
        m = self._require_model(model_name)
        version_str = str(version)

        if version_str in m.versions:
            raise ValueError(f"Version already exists: {model_name}@{version_str}")

        m.versions[version_str] = version
        
    def store_artifact(self, model_name: str, version: str, filename: str, src_path: Path) -> Path:
        m = self._require_model(model_name)
        if version not in m.versions:
            raise ValueError(f"Unknown model version: {model_name}@{version}")

        ref = ArtifactRef(model_name=model_name, version=version, filename=filename)
        stored_path = self._artifact_store.put(ref, src_path)
        m.artifacts[(version, filename)] = ref
        return stored_path

    def resolve_artifact(self, model_name: str, version: str, filename: str) -> Path:
        m = self._require_model(model_name)
        key = (version, filename)
        if key not in m.artifacts:
            # If registry has no mapping, still allow direct lookup by convention.
            ref = ArtifactRef(model_name=model_name, version=version, filename=filename)
            return self._artifact_store.get(ref)

        return self._artifact_store.get(m.artifacts[key])

    def _require_model(self, model_name: str) -> RegisteredModel:
        if model_name not in self._models:
            raise ValueError(f"Model not registered: {model_name}")
        return self._models[model_name]
