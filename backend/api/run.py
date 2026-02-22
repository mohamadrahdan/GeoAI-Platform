from __future__ import annotations
from typing import Any, Dict, Optional
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from core.plugins.errors import PluginError, PluginExecutionError, PluginTimeoutError
from core.plugins.executor import PluginExecutor
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import numpy as np

router = APIRouter()

class RunRequest(BaseModel):
    payload: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: Optional[float] = None

@router.post("/run/{plugin_name}")
def run_plugin(plugin_name: str, body: RunRequest, request: Request) -> dict:
    container = request.app.state.container
    registry = container.plugin_registry

    if registry is None:
        raise HTTPException(status_code=500, detail="Plugin registry not initialized")

    executor = PluginExecutor(registry=registry, logger=container.logger)

    try:
        result = executor.run_with_timeout(
            plugin_name=plugin_name,
            payload=body.payload,
            timeout_seconds=body.timeout_seconds,
        )

        payload = {"status": "ok", "plugin": plugin_name, "result": result}

        encoded = jsonable_encoder(
            payload,
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
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_name}' not found")
    except PluginError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
