from core.models.metadata import ModelMetadata, ModelVersion

def test_model_version_to_string():
    assert str(ModelVersion(1, 2, 3)) == "1.2.3"
    assert str(ModelVersion(1, 2, 3, build="cuda12")) == "1.2.3+cuda12"

    
def test_model_metadata_is_immutable():
    meta = ModelMetadata(
        name="unet_landslide",
        task="segmentation",
        framework="pytorch",
        version=ModelVersion(0, 1, 0),
        schema_version="v1",
        artifact_uri="file://models/unet.pt",
        extra={"input_size": 512},
    )
    assert meta.name == "unet_landslide"
    assert meta.extra["input_size"] == 512
