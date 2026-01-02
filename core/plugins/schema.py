from typing import Any, Dict, TypedDict


class PluginInput(TypedDict):
    params: Dict[str, Any]


class PluginOutput(TypedDict):
    status: str
    result: Dict[str, Any]
