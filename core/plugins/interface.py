# Plugin contract definition
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict


class BasePlugin(ABC):
    """
    Base interface for all plugins.
    Plugins must be stateless or manage their own internal state
    """
    name: str
    version: str

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = config or {}

    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute plugin logic.
        Args:payload: validated input data
        Returns:result dictionary
        """
        raise NotImplementedError

    def shutdown(self) -> None:
        """
        Optional cleanup hook
        """
        return None
