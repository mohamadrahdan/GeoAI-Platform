from core.models.registry import ModelRegistry
from core.models.metadata import ModelMetadata, ModelVersion

def test_registry_register_and_get():
    registry = ModelRegistry()

    metadata = ModelMetadata(
        name="unet_landslide",
        task="segmentation",
        framework="pytorch",
        version=ModelVersion(1, 0, 0),
        schema_version="v1",
    )

    registry.register(metadata)

    retrieved = registry.get("unet_landslide", "1.0.0")
    assert retrieved.name == "unet_landslide"

def test_registry_prevents_duplicate_versions():
    registry = ModelRegistry()

    metadata = ModelMetadata(
        name="unet_landslide",
        task="segmentation",
        framework="pytorch",
        version=ModelVersion(1, 0, 0),
        schema_version="v1",
    )

    registry.register(metadata)

    try:
        registry.register(metadata)
        assert False
    except ValueError:
        assert True
