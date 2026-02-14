import numpy as np
from core.models.base import BaseModel
from core.models.metadata import ModelMetadata, ModelVersion
from core.models.contracts import ModelInput, ModelOutput, SpatialMetadata

class DummyModel(BaseModel):
    def __init__(self, metadata: ModelMetadata) -> None:
        super().__init__(metadata)
        self.loaded_called = 0
        self.predict_called = 0
        self.released_called = 0

    def on_load(self) -> None:
        self.loaded_called += 1

    def on_predict(self, x: ModelInput) -> ModelOutput:
        self.predict_called += 1
        return ModelOutput(prediction=np.zeros((1, 4, 4)), spatial=x.spatial)

    def on_release(self) -> None:
        self.released_called += 1

def test_lifecycle_enforces_load_and_is_idempotent():
    md = ModelMetadata(
    name="dummy",
    task="segmentation",
    framework="none",
    version=ModelVersion(0, 0, 1),
    schema_version="v1",
)
    model = DummyModel(md)
    spatial = SpatialMetadata(crs="EPSG:4326", bbox=(0, 0, 1, 1), resolution=10.0)
    x = ModelInput(data=np.zeros((1, 4, 4)), bands=["B02"], spatial=spatial)

    # predict should trigger load automatically
    _ = model.predict(x)
    assert model.is_loaded is True
    assert model.loaded_called == 1
    assert model.predict_called == 1

    # load again should not re-load
    model.load()
    assert model.loaded_called == 1

    # release is idempotent
    model.release()
    assert model.is_loaded is False
    assert model.released_called == 1

    model.release()
    assert model.released_called == 1
