import pytest
from core.models.registry import ModelRegistry
from core.models.metadata import ModelMetadata, ModelVersion
from core.models.artifacts import LocalArtifactStore


def test_registry_register_and_version(tmp_path):
    # Initialize the store and registry exactly as Phase 4 architecture dictates
    store = LocalArtifactStore(root_dir=tmp_path)
    registry = ModelRegistry(artifact_store=store)
    # Initialize ModelMetadata with the exact required arguments from your codebase
    meta = ModelMetadata(
        name="test-model",
        task="segmentation",
        framework="pytorch",
        version=ModelVersion(1, 0, 0),
        schema_version="v1",
    )
    # Use the correct Phase 4 methods
    registry.register_model(meta)
    registry.add_version("test-model", meta.version)
    # Test resolving the version instead of fetching a model instance
    resolved = registry.resolve_version("test-model", "1.0.0")
    assert resolved.major == 1
    assert resolved.minor == 0
    assert resolved.patch == 0


def test_registry_prevents_duplicate_versions(tmp_path):
    store = LocalArtifactStore(root_dir=tmp_path)
    registry = ModelRegistry(artifact_store=store)
    meta = ModelMetadata(
        name="duplicate-model",
        task="segmentation",
        framework="pytorch",
        version=ModelVersion(1, 0, 0),
        schema_version="v1",
    )

    registry.register_model(meta)
    registry.add_version("duplicate-model", meta.version)

    # Adding the exact same version again should raise ValueError
    with pytest.raises(ValueError):
        registry.add_version("duplicate-model", meta.version)
