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
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from core.common.exceptions import InferenceTimeoutError, ExecutionError

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
        timings: Dict[str, float] = {}

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

        # predict(Read optional timeout from request parameters)
        timeout_s_raw = req.parameters.get("timeout_s") if isinstance(req.parameters, dict) else None
        timeout_s = float(timeout_s_raw) if timeout_s_raw is not None else None

        s = perf_counter()
        try:
            if timeout_s is None:
                y = model.predict(x)
            else:
                # Run predict in a separate thread to enforce a hard timeout
                with ThreadPoolExecutor(max_workers=1) as ex:
                    fut = ex.submit(model.predict, x)
                    try:
                        y = fut.result(timeout=timeout_s)
                    except FuturesTimeoutError as e:
                        raise InferenceTimeoutError(
                            f"Inference timed out after {timeout_s:.3f}s for {req.model_name}@{version_str}"
                        ) from e

            log_event("predict", s, ok=True)

        except InferenceTimeoutError as e:
            log_event("predict", s, ok=False, detail=str(e))
            raise

        except Exception as e:
            log_event("predict", s, ok=False, detail=f"{type(e).__name__}: {e}")
            raise ExecutionError(f"Inference execution failed for {req.model_name}@{version_str}") from e

        # build timings from events
        for ev in events:
            timings[ev.name] = ev.ms

        # compute total execution time
        total_ms = (perf_counter() - t0) * 1000.0
        timings["total"] = total_ms

        # final log
        self._ctx.logger.info(
            "trace=%s stage=end ok=1 total_ms=%.2f model=%s version=%s request_id=%s",
            trace_id,
            total_ms,
            req.model_name,
            version_str,
            req.request_id,
        )

        total_ms = (perf_counter() - t0) * 1000
        timings["total"] = total_ms

        self._ctx.logger.info(
            "trace=%s stage=end ok=1 total_ms=%.2f model=%s version=%s request_id=%s",
            trace_id,
            total_ms,
            req.model_name,
            version_str,
            req.request_id,
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
