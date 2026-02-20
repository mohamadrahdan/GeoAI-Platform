from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter
from typing import Dict
from core.common.exceptions import ExecutionError
from core.data_manager.base import BaseDataManager
from core.logging.logger import Logger
from core.models.registry import ModelRegistry
from core.inference.io import load_input_from_request
from core.inference.providers import BaseModelProvider
from core.inference.schemas import InferenceRequest, InferenceResponse
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from core.common.exceptions import DataAccessError, ExecutionError, InferenceTimeoutError

@dataclass(frozen=True)
class InferenceContext:
    "Dependencies required to execute inference"

    registry: ModelRegistry
    model_provider: BaseModelProvider
    data_manager: BaseDataManager
    logger: Logger


class InferenceEngine:
    def __init__(self, ctx: InferenceContext) -> None:
        self._ctx = ctx

    def execute(self, req: InferenceRequest) -> InferenceResponse:
        "Execute an inference request end-to-end"
        t0 = perf_counter()

        req.validate_input()

        # Validate request
        try:
            req.validate_input()
        except Exception as e:
            raise ExecutionError("Invalid inference request.") from e
        
        # Resolve model version
        version_strategy = "latest" if req.version.strategy == "latest" else (req.version.value or "")
        try:
            resolved = self._ctx.registry.resolve_version(req.model_name, version_strategy)
        except Exception as e:
            raise ExecutionError(
                f"Failed to resolve version for {req.model_name} using strategy={version_strategy}"
            ) from e

        version_str = str(resolved)

        # Get model instance
        try:
            model = self._ctx.model_provider.get(req.model_name, version_str)
        except Exception as e:
            raise ExecutionError(f"Failed to load model instance: {req.model_name}@{version_str}") from e

        t_resolve = perf_counter()

        # Load input
        try:
            x = load_input_from_request(req=req, data_manager=self._ctx.data_manager)
        except DataAccessError:
            # keep the original type for callers (API layer can map it)
            raise
        except Exception as e:
            raise DataAccessError("Failed to load inference input.") from e

        t_input = perf_counter()
        
        # Predict
        timeout_s = None
        if isinstance(req.parameters, dict):
            timeout_s = req.parameters.get("timeout_s")

        try:
            if timeout_s is None:
                y = model.predict(x)
            else:
                with ThreadPoolExecutor(max_workers=1) as ex:
                    fut = ex.submit(model.predict, x)
                    try:
                        y = fut.result(timeout=float(timeout_s))
                    except FuturesTimeoutError as e:
                        raise InferenceTimeoutError(
                            f"Inference timed out after {timeout_s}s for "
                            f"{req.model_name}@{version_str}"
                        ) from e

        except InferenceTimeoutError:
            self._ctx.logger.error(
                "Inference timeout model=%s version=%s request_id=%s",
                req.model_name,
                version_str,
                req.request_id,
            )
            raise

        except Exception as e:
            self._ctx.logger.exception(
                "Inference failed model=%s version=%s request_id=%s",
                req.model_name,
                version_str,
                req.request_id,
            )
            raise ExecutionError(
                f"Inference execution failed for {req.model_name}@{version_str}"
            ) from e

        t_pred = perf_counter()

        timings: Dict[str, float] = {
            "resolve_model": (t_resolve - t0) * 1000.0,
            "load_input": (t_input - t_resolve) * 1000.0,
            "predict": (t_pred - t_input) * 1000.0,
            "total": (t_pred - t0) * 1000.0,
        }

        self._ctx.logger.info(
            "Inference executed model=%s version=%s total_ms=%.2f",
            req.model_name,
            version_str,
            timings["total"],
        )

        return InferenceResponse(
            request_id=req.request_id,
            model_name=req.model_name,
            version=version_str,
            output=y,
            timings_ms=timings,
            tags=req.tags,
        )
