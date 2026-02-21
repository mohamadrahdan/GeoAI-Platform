import numpy as np
from core.models.contracts import ModelOutput, SpatialMetadata
from core.evaluation.basic_metrics import AccuracyMetric, IoUMetric, DiceMetric

def _make_output(arr: np.ndarray) -> ModelOutput:
    spatial = SpatialMetadata(crs="EPSG:4326", bbox=(0, 0, 1, 1), resolution=10.0)
    return ModelOutput(prediction=arr, spatial=spatial)

def test_accuracy_metric():
    pred = np.array([[1, 0], [1, 0]], dtype=np.float32)
    true = np.array([[1, 0], [0, 0]], dtype=np.float32)
    metric = AccuracyMetric()
    result = metric.compute(_make_output(pred), true)
    assert result.name == "accuracy"
    assert 0.0 <= result.value <= 1.0

def test_iou_metric():
    pred = np.array([[1, 0], [1, 0]], dtype=np.float32)
    true = np.array([[1, 0], [0, 0]], dtype=np.float32)
    metric = IoUMetric()
    result = metric.compute(_make_output(pred), true)
    assert result.name == "iou"
    assert 0.0 <= result.value <= 1.0

def test_dice_metric():
    pred = np.array([[1, 0], [1, 0]], dtype=np.float32)
    true = np.array([[1, 0], [0, 0]], dtype=np.float32)
    metric = DiceMetric()
    result = metric.compute(_make_output(pred), true)
    assert result.name == "dice"
    assert 0.0 <= result.value <= 1.0