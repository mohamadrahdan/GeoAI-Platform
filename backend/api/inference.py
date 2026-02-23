from __future__ import annotations
from typing import Optional
import numpy as np
from fastapi import APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from core.inference.schemas import InferenceRequest
from core.plugins.executor import PluginExecutor
from core.plugins.errors import PluginError, PluginExecutionError, PluginTimeoutError

router = APIRouter()
class UnifiedInferenceRequest(BaseModel):
    "Public API request for inference(this is executed via the model_adapter plugin)"
    request: InferenceRequest
    model_class: Optional[str] = Field(
        default=None,
        description="Optional dotted path for a runtime-loadable model class "
                    "(e.g., plugins.model_adapter.dummy_model.DummyModel).",
    )
    timeout_seconds: Optional[float] = Field(default=None)

@router.post("/inference")
def unified_inference(body: UnifiedInferenceRequest, request: Request):
    container = request.app.state.container
    registry = container.plugin_registry
    if registry is None:
        raise HTTPException(status_code=500, detail="Plugin registry not initialized")
    executor = PluginExecutor(registry=registry, logger=container.logger)
    plugin_payload = {
        "model_class": body.model_class,
        "request": body.request.model_dump(),
    }
    try:
        result = executor.run_with_timeout(
            plugin_name="model_adapter",
            payload=plugin_payload,
            timeout_seconds=body.timeout_seconds,
        )
        response_payload = {
            "status": "ok",
            "mode": "unified_inference",
            "plugin": "model_adapter",
            "result": result,
        }
        encoded = jsonable_encoder(
            response_payload,
            custom_encoder={
                np.ndarray: lambda a: a.tolist(),
                np.generic: lambda a: a.item(),
            },
        )
        return JSONResponse(content=encoded)

    except PluginTimeoutError as exc:
        raise HTTPException(status_code=408, detail=str(exc)) from exc
    except PluginExecutionError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except KeyError:
        raise HTTPException(status_code=404, detail="Plugin 'model_adapter' not found")  # should not happen if /plugins shows it
    except PluginError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc