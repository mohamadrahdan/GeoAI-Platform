from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

class BaseDataManager(ABC):
    """
    Abstract interface for data access.
    Plugins must NOT access filesystem directly.
    """

    @abstractmethod
    def resolve(self, relative_path: str) -> Path:
        "Resolve a relative path inside the data root."
        raise NotImplementedError

    @abstractmethod
    def exists(self, relative_path: str) -> bool:
        "Check if a data object exists."
        raise NotImplementedError

    @abstractmethod
    def load(self, relative_path: str) -> Any:
        "Load data from storage."
        raise NotImplementedError

    @abstractmethod
    def save(self, relative_path: str, data: Any) -> None:
        "Save data to storage."
        raise NotImplementedError

