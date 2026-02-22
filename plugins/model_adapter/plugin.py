from __future__ import annotations
import numpy as np
from typing import Any
from importlib import import_module
from typing import Any, Dict, Optional, Tuple
from core.plugins.interface import BasePlugin
from core.services import get_container
from core.inference.engine import InferenceContext, InferenceEngine
from core.inference.providers import InMemoryModelProvider
from core.inference.schemas import InferenceRequest, VersionSpec

# Module-level cache so provider/models can survive within the Python process
_PROVIDER: Optional[InMemoryModelProvider] = None

def _load_class(dotted_path: str):
    "Load class from dotted path like plugins.landslide.model.some_model.MyModel"
    module_path, cls_name = dotted_path.rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, cls_name)

def _to_jsonable(obj: Any) -> Any:
    "Convert common non-JSON types (e.g., numpy) into JSON-serializable structures"
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(v) for v in obj]
    return obj

class ModelAdapterPlugin(BasePlugin):
    """
    Wraps a BaseModel instance behind the existing plugin execution system.
    Payload contract (MVP):
    {
      "model_class": "some.dotted.path.MyModel",   # optional (if you want to register a model instance here)
      "request": {
          "model_name": "dummy_model",
          "version": {"strategy": "latest"} | {"strategy": "exact", "value": "1.0.0"},
          "input_uri": "...",                      # optional
          "input_payload": {...},                  # optional
          "parameters": {...},                     # optional
          "request_id": "...",                     # optional
          "tags": {...}                            # optional
      }
    }
    """
    name = "model_adapter"
    version = "0.1.0"
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        c = get_container()
        global _PROVIDER
        if _PROVIDER is None:
            _PROVIDER = InMemoryModelProvider(registry=c.registry)
        # Optional: register model instance dynamically (useful for tests/local)
        model_class_path = payload.get("model_class")
        if model_class_path:
            ModelCls = _load_class(model_class_path)
            model_instance = ModelCls()
            _PROVIDER.register(model_instance)
        req_dict = payload.get("request")
        if not isinstance(req_dict, dict):
            raise ValueError("payload.request must be a dict")

        # Build InferenceRequest (matches core/inference/schemas.py)
        version_dict = req_dict.get("version") or {}
        version = VersionSpec(
            strategy=version_dict.get("strategy", "latest"),
            value=version_dict.get("value"),
        )
        req = InferenceRequest(
            model_name=req_dict["model_name"],
            version=version,
            input_uri=req_dict.get("input_uri"),
            input_payload=req_dict.get("input_payload"),
            parameters=req_dict.get("parameters") or {},
            request_id=req_dict.get("request_id"),
            tags=req_dict.get("tags") or {},
        )
        ctx = InferenceContext(
            registry=c.registry,
            model_provider=_PROVIDER,
            data_manager=c.data_manager,
            logger=c.logger,
        )
        engine = InferenceEngine(ctx)
        resp = engine.execute(req)

        # Return a plugin-friendly dict
        return {
            "request_id": resp.request_id,
            "trace_id": resp.trace_id,
            "model_name": resp.model_name,
            "version": resp.version,
            "output": resp.output,
            "timings_ms": resp.timings_ms,
            "tags": resp.tags,
            "events": [e.model_dump() for e in resp.events],
            "output": resp.output,
        }