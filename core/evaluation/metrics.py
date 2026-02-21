from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional
import numpy as np
from core.models.contracts import ModelOutput


@dataclass(frozen=True)
class MetricResult:
    """
    Standard metric output.
    - name: metric identifier (stable)
    - value: primary scalar value (float)
    - details: optional extra info for debugging/analysis
    """
    name: str
    value: float
    details: Optional[Dict[str, Any]] = None

class BaseMetric(ABC):
    """
    A framework-agnostic metric interface for evaluating model outputs.
    Notes:
    - y_pred is a ModelOutput (prediction stored in y_pred.prediction)
    - y_true is a numpy array (e.g., segmentation mask), shape should match prediction
    """
    @property
    @abstractmethod
    def name(self) -> str:
        "Stable metric name (e.g., 'iou', 'dice')."
        raise NotImplementedError
    @property
    def higher_is_better(self) -> bool:
        "Whether higher values indicate better performance."
        return True
    @abstractmethod
    def compute(self, y_pred: ModelOutput, y_true: np.ndarray) -> MetricResult:
        "Compute the metric and return a MetricResult."
        raise NotImplementedError