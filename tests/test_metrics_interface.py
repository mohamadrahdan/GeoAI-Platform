import numpy as np
from core.evaluation.metrics import BaseMetric, MetricResult
from core.models.contracts import ModelOutput, SpatialMetadata

class DummyMetric(BaseMetric):
    @property
    def name(self) -> str:
        return "dummy"
    def compute(self, y_pred: ModelOutput, y_true: np.ndarray) -> MetricResult:
        # Return a deterministic value for testing
        return MetricResult(name=self.name, value=1.0, details={"ok": True})

def test_metric_result_is_constructible() -> None:
    r = MetricResult(name="iou", value=0.5, details={"threshold": 0.5})
    assert r.name == "iou"
    assert r.value == 0.5
    assert r.details == {"threshold": 0.5}

def test_dummy_metric_compute_returns_metric_result() -> None:
    spatial = SpatialMetadata(crs="EPSG:4326", bbox=(0, 0, 1, 1), resolution=10.0)
    pred = ModelOutput(prediction=np.zeros((1, 4, 4), dtype=np.float32), spatial=spatial)
    y_true = np.zeros((1, 4, 4), dtype=np.float32)

    m = DummyMetric()
    out = m.compute(pred, y_true)
    assert out.name == "dummy"
    assert out.value == 1.0
    assert out.details == {"ok": True}