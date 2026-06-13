from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter
from typing import List, Optional, Any
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from core.common.exceptions import (
    DataAccessError,
    InferenceTimeoutError,
    ExecutionError,
)
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

    def execute(self, req: InferenceRequest) -> InferenceResponse:
        t0 = perf_counter()
        trace_id = self._make_trace_id(req)
        events: List[TraceEvent] = []

        # 1. Pipeline Execution
        try:
            s_val = perf_counter()
            req.validate_input()
            self._log_event("validate", s_val, trace_id, req, events)
            version_str = self._resolve_version(req, trace_id, events)
            model = self._load_model(req, version_str, trace_id, events)
            x = self._load_input(req, trace_id, events)
            y = self._predict(req, model, x, version_str, trace_id, events)
        except (DataAccessError, InferenceTimeoutError):
            raise
        except Exception as e:
            raise ExecutionError(f"Inference failed: {str(e)}") from e

        # 2. Finalize
        return self._build_response(req, trace_id, y, version_str, events, t0)

    def _make_trace_id(self, req: InferenceRequest) -> str:
        return req.request_id.strip() if req.request_id else uuid4().hex[:12]

    def _resolve_version(
        self, req: InferenceRequest, trace_id: str, events: List[TraceEvent]
    ) -> str:
        s = perf_counter()
        try:
            strategy = (
                "latest"
                if req.version.strategy == "latest"
                else (req.version.value or "")
            )
            resolved = self._ctx.registry.resolve_version(req.model_name, strategy)
            self._log_event(
                "resolve_version", s, trace_id, req, events, detail=str(resolved)
            )
            return str(resolved)
        except Exception as e:
            self._log_event(
                "resolve_version", s, trace_id, req, events, ok=False, detail=str(e)
            )
            raise ExecutionError(f"Version resolution failed for {req.model_name}")

    def _load_model(
        self,
        req: InferenceRequest,
        version: str,
        trace_id: str,
        events: List[TraceEvent],
    ) -> Any:
        s = perf_counter()
        try:
            model = self._ctx.model_provider.get(req.model_name, version)
            self._log_event("load_model", s, trace_id, req, events)
            return model
        except Exception as e:
            self._log_event(
                "load_model", s, trace_id, req, events, ok=False, detail=str(e)
            )
            raise ExecutionError(f"Model load failed: {req.model_name}")

    def _load_input(
        self, req: InferenceRequest, trace_id: str, events: List[TraceEvent]
    ) -> Any:
        s = perf_counter()
        try:
            x = load_input_from_request(req=req, data_manager=self._ctx.data_manager)
            self._log_event("load_input", s, trace_id, req, events)
            return x
        except Exception as e:
            self._log_event(
                "load_input", s, trace_id, req, events, ok=False, detail=str(e)
            )
            raise DataAccessError("Failed to load input.")

    def _predict(
        self,
        req: InferenceRequest,
        model: Any,
        x: Any,
        version: str,
        trace_id: str,
        events: List[TraceEvent],
    ) -> Any:
        s = perf_counter()
        timeout = self._get_timeout(req)
        try:
            if timeout is None:
                y = model.predict(x)
            else:
                with ThreadPoolExecutor(max_workers=1) as ex:
                    y = ex.submit(model.predict, x).result(timeout=timeout)
            self._log_event("predict", s, trace_id, req, events)
            return y
        except FuturesTimeoutError as e:
            self._log_event(
                "predict", s, trace_id, req, events, ok=False, detail="Timeout"
            )
            raise InferenceTimeoutError(f"Timed out after {timeout}s") from e
        except Exception as e:
            self._log_event(
                "predict", s, trace_id, req, events, ok=False, detail=str(e)
            )
            raise ExecutionError("Prediction failed")

    def _get_timeout(self, req: InferenceRequest) -> Optional[float]:
        val = (
            req.parameters.get("timeout_s")
            if isinstance(req.parameters, dict)
            else None
        )
        return float(val) if val is not None else None

    def _log_event(
        self,
        name: str,
        start: float,
        trace_id: str,
        req: InferenceRequest,
        events: List[TraceEvent],
        ok: bool = True,
        detail: Optional[str] = None,
    ) -> None:
        ms = (perf_counter() - start) * 1000.0
        events.append(TraceEvent(name=name, ms=ms, ok=ok, detail=detail))
        log_func = self._ctx.logger.info if ok else self._ctx.logger.error
        log_func(
            "trace=%s stage=%s ok=%d ms=%.2f model=%s request_id=%s detail=%s",
            trace_id,
            name,
            int(ok),
            ms,
            req.model_name,
            req.request_id,
            detail,
        )

    def _build_response(
        self,
        req: InferenceRequest,
        trace_id: str,
        y: Any,
        version: str,
        events: List[TraceEvent],
        t0: float,
    ) -> InferenceResponse:
        timings = {ev.name: ev.ms for ev in events}
        timings["total"] = (perf_counter() - t0) * 1000.0

        self._ctx.logger.info(
            "trace=%s stage=end total_ms=%.2f", trace_id, timings["total"]
        )
        return InferenceResponse(
            request_id=req.request_id,
            trace_id=trace_id,
            model_name=req.model_name,
            version=version,
            output=y,
            timings_ms=timings,
            events=events,
            tags=req.tags,
        )
