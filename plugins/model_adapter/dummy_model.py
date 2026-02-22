from __future__ import annotations
import numpy as np
from core.models.base import BaseModel
from core.models.metadata import ModelMetadata, ModelVersion
from core.models.contracts import ModelInput, ModelOutput

class DummyModel(BaseModel):
    def __init__(self) -> None:
        meta = ModelMetadata(
            name="dummy_model",
            task="demo",
            framework="numpy",
            version=ModelVersion(1, 0, 0),
            schema_version="v1",
        )
        super().__init__(metadata=meta)

    def on_load(self) -> None:
        # No-op for dummy model
        return

    def on_predict(self, x: ModelInput) -> ModelOutput:
        # Output: a 1xHxW mask filled with ones (float32)
        _, h, w = x.data.shape
        pred = np.ones((1, h, w), dtype=np.float32)
        return ModelOutput(prediction=pred, spatial=x.spatial)