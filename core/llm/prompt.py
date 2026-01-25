from __future__ import annotations
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PromptTemplate:
    "Minimal prompt template with safe formatting"
    name: str
    template: str
    def render(self, variables: Dict[str, str]) -> str:
        # Using str.format is ok here for MVP; keep variables controlled.
        try:
            return self.template.format(**variables)
        except KeyError as exc:
            missing = str(exc).strip("'")
            raise KeyError(f"Missing prompt variable: {missing}") from exc

# A tiny built-in catalog (can be extended later)
SYSTEM_SUMMARY = PromptTemplate(
    name="system_summary",
    template=(
        "You are a GeoAI assistant.\n"
        "Task: {task}\n"
        "Context: {context}\n"
        "Return a concise, structured answer."
    ),
)
