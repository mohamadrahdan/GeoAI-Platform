# core/llm/engine.py

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

from core.llm.context import LLMContext


@dataclass(frozen=True)
class LLMResponse:
    "Minimal response object for LLM calls"
    text: str
    raw: Optional[Dict[str, Any]] = None


class BaseLLMEngine(ABC):
    "Provider-agnostic LLM engine abstraction"
    @abstractmethod
    def generate(self, prompt: str, context: Optional[LLMContext] = None) -> LLMResponse:
        "Generate a response given a prompt and optional context"
        raise NotImplementedError


class NullLLMEngine(BaseLLMEngine):
    """
    Placeholder engine (MVP): returns a deterministic message.
    Useful for wiring and tests before integrating a real provider.
    """
    def generate(self, prompt: str, context: Optional[LLMContext] = None) -> LLMResponse:
        return LLMResponse(
            text="LLM engine is not configured yet. This is a placeholder response.",
            raw={"prompt_preview": prompt[:120], "has_context": context is not None},
        )
