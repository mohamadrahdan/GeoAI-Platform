from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter
from typing import Dict, List, Optional
from uuid import uuid4
from core.common.exceptions import DataAccessError, ExecutionError, InferenceTimeoutError
from core.data_manager.base import BaseDataManager
from core.logging.logger import Logger
from core.models.registry import ModelRegistry
from core.inference.io import load_input_from_request
from core.inference.providers import BaseModelProvider
from core.inference.schemas import InferenceRequest, InferenceResponse, TraceEvent

@dataclass(frozen=True)
class InferenceContext:
    registry: ModelRegistry
    model_provider: BaseModelProvider
    data_manager: BaseDataManager
    logger: Logger

class InferenceEngine:
    def __init__(self, ctx: InferenceContext) -> None:
        self._ctx = ctx

    def _make_trace_id(self, req: InferenceRequest) -> str:
        # Prefer request_id if provided; otherwise generate a stable trace_id
        base = req.request_id.strip() if req.request_id else ""
        if base:
            return base
        return uuid4().hex[:12]

    def execute(self, req: InferenceRequest) -> InferenceResponse:
        t0 = perf_counter()
        trace_id = self._make_trace_id(req)
        events: List[TraceEvent] = []

        def log_event(name: str, start: float, ok: bool = True, detail: Optional[str] = None) -> None:
            ms = (perf_counter() - start) * 1000.0
            events.append(TraceEvent(name=name, ms=ms, ok=ok, detail=detail))
            # Key-value style (works with std logging formatter)
            if ok:
                self._ctx.logger.info(
                    "trace=%s stage=%s ok=1 ms=%.2f model=%s request_id=%s",
                    trace_id, name, ms, req.model_name, req.request_id
                )
            else:
                self._ctx.logger.error(
                    "trace=%s stage=%s ok=0 ms=%.2f model=%s request_id=%s detail=%s",
                    trace_id, name, ms, req.model_name, req.request_id, detail
                )
        self._ctx.logger.info(
            "trace=%s stage=start ok=1 model=%s request_id=%s",
            trace_id, req.model_name, req.request_id
        )

        # validate
        s = perf_counter()
        try:
            req.validate_input()
            log_event("validate", s, ok=True)
        except Exception as e:
            log_event("validate", s, ok=False, detail=f"{type(e).__name__}: {e}")
            raise ExecutionError("Invalid inference request.") from e
        
        # resolve_version
        s = perf_counter()
        try:
            version_strategy = "latest" if req.version.strategy == "latest" else (req.version.value or "")
            resolved = self._ctx.registry.resolve_version(req.model_name, version_strategy)
            version_str = str(resolved)
            log_event("resolve_version", s, ok=True, detail=version_str)
        except Exception as e:
            log_event("resolve_version", s, ok=False, detail=f"{type(e).__name__}: {e}")
            raise ExecutionError(
                f"Failed to resolve model version for {req.model_name} (strategy={version_strategy})"
            ) from e

        # load_model
        s = perf_counter()
        try:
            model = self._ctx.model_provider.get(req.model_name, version_str)
            log_event("load_model", s, ok=True)
        except Exception as e:
            log_event("load_model", s, ok=False, detail=f"{type(e).__name__}: {e}")
            raise ExecutionError(f"Failed to load model instance: {req.model_name}@{version_str}") from e

        # load_input
        s = perf_counter()
        try:
            x = load_input_from_request(req=req, data_manager=self._ctx.data_manager)
            log_event("load_input", s, ok=True)
        except DataAccessError as e:
            log_event("load_input", s, ok=False, detail=f"{type(e).__name__}: {e}")
            raise
        except Exception as e:
            log_event("load_input", s, ok=False, detail=f"{type(e).__name__}: {e}")
            raise DataAccessError("Failed to load inference input.") from e

        # predict (timeout handled already in 4.3.3 if you added it)
        s = perf_counter()
        try:
            y = model.predict(x)
            log_event("predict", s, ok=True)
        except InferenceTimeoutError as e:
            log_event("predict", s, ok=False, detail=f"{type(e).__name__}: {e}")
            raise
        except Exception as e:
            log_event("predict", s, ok=False, detail=f"{type(e).__name__}: {e}")
            raise ExecutionError(f"Inference execution failed for {req.model_name}@{version_str}") from e
        t_end = perf_counter()
        timings: Dict[str, float] = {
            "total": (t_end - t0) * 1000.0,
        }

        # optional: stage totals from events (if you want)
        for ev in events:
            timings[ev.name] = ev.ms
        self._ctx.logger.info(
            "trace=%s stage=end ok=1 total_ms=%.2f model=%s version=%s request_id=%s",
            trace_id, timings["total"], req.model_name, version_str, req.request_id
        )

        return InferenceResponse(
            request_id=req.request_id,
            trace_id=trace_id,
            model_name=req.model_name,
            version=version_str,
            output=y,
            timings_ms=timings,
            events=events,
            tags=req.tags,
        )