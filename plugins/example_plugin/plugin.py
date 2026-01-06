from __future__ import annotations

from typing import Any, Dict

from core.plugins.interface import BasePlugin

class ExamplePlugin(BasePlugin):
    name = "example_plugin"
    version = "0.1.0"
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Minimal executable example: echo + simple transform
        message = str(payload.get("message", "hello"))
        return {
            "echo": message,
            "length": len(message),
        }
