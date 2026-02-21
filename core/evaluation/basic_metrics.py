from __future__ import annotations
from typing import Optional, Dict, Any
import numpy as np
from core.evaluation.metrics import BaseMetric, MetricResult
from core.models.contracts import ModelOutput

def _binarize(x: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    return (x >= threshold).astype(np.uint8)

class AccuracyMetric(BaseMetric):
    @property
    def name(self) -> str:
        return "accuracy"
    def compute(self, y_pred: ModelOutput, y_true: np.ndarray) -> MetricResult:
        y_hat = _binarize(y_pred.prediction)
        y_true_bin = _binarize(y_true)
        correct = np.sum(y_hat == y_true_bin)
        total = y_true_bin.size
        acc = float(correct) / float(total)

        return MetricResult(
            name=self.name,
            value=acc,
            details={"correct": int(correct), "total": int(total)},
        )

class IoUMetric(BaseMetric):
    @property
    def name(self) -> str:
        return "iou"
    def compute(self, y_pred: ModelOutput, y_true: np.ndarray) -> MetricResult:
        y_hat = _binarize(y_pred.prediction)
        y_true_bin = _binarize(y_true)
        intersection = np.logical_and(y_hat, y_true_bin).sum()
        union = np.logical_or(y_hat, y_true_bin).sum()

        if union == 0:
            iou = 1.0  # both empty
        else:
            iou = float(intersection) / float(union)

        return MetricResult(
            name=self.name,
            value=iou,
            details={
                "intersection": int(intersection),
                "union": int(union),
            },
        )

class DiceMetric(BaseMetric):
    @property
    def name(self) -> str:
        return "dice"
    def compute(self, y_pred: ModelOutput, y_true: np.ndarray) -> MetricResult:
        y_hat = _binarize(y_pred.prediction)
        y_true_bin = _binarize(y_true)
        intersection = np.logical_and(y_hat, y_true_bin).sum()
        total = y_hat.sum() + y_true_bin.sum()

        if total == 0:
            dice = 1.0
        else:
            dice = 2.0 * float(intersection) / float(total)

        return MetricResult(
            name=self.name,
            value=dice,
            details={
                "intersection": int(intersection),
                "sum_pred_true": int(total),
            },
        )