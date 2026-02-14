from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from core.models.metadata import ModelMetadata
from core.models.contracts import ModelInput, ModelOutput

class BaseModel(ABC):
    "Framework-agnostic base model with lifecycle hooks"
    def __init__(self, metadata: ModelMetadata) -> None:
        self._metadata = metadata
        self._is_loaded: bool = False

    @property
    def metadata(self) -> ModelMetadata:
        return self._metadata

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def load(self) -> None:
        "Load model weights/resources. Safe to call multiple times"
        if self._is_loaded:
            return
        self.on_load()
        self._is_loaded = True

    def warmup(self) -> None:
        "Optional warmup step to reduce cold-start latency"
        if not self._is_loaded:
            self.load()
        self.on_warmup()

    def predict(self, x: ModelInput) -> ModelOutput:
        "Enforces lifecycle: must be loaded before inference"
        if not self._is_loaded:
            self.load()
        self.on_before_predict(x)
        y = self.on_predict(x)
        self.on_after_predict(y)
        return y

    def release(self) -> None:
        "Release resources. Safe to call multiple times"
        if not self._is_loaded:
            return
        self.on_release()
        self._is_loaded = False

    #Hooks (override in concrete models)
    @abstractmethod
    def on_load(self) -> None:
        pass
    def on_warmup(self) -> None:
        pass
    def on_before_predict(self, x: ModelInput) -> None:
        pass
    @abstractmethod
    def on_predict(self, x: ModelInput) -> ModelOutput:
        pass
    def on_after_predict(self, y: ModelOutput) -> None:
        pass
    def on_release(self) -> None:
        pass
