from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class ModelId:
    "Unique identifier for a model instance"
    name: str
    version: str

class BaseModel(ABC):
    "Core abstraction for all models in the GeoAI Platform"
    def __init__(self, model_id: ModelId) -> None:
        self.model_id = model_id
        self._is_loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @abstractmethod
    def load(self) -> None:
        "Load model weights or initialize resources"
        ...

    @abstractmethod
    def predict(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        "Perform inference"
        ...

    @abstractmethod
    def unload(self) -> None:
        "Release memory / GPU resources"
        ...
