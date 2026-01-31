from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, TypeVar, Optional
from core.logging.logger import get_module_logger

logger = get_module_logger(__name__)

T = TypeVar("T")

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_sec: float = 0.5
    max_delay_sec: float = 5.0

def run_with_retries(fn: Callable[[], T], policy: RetryPolicy, op_name: str, context: Optional[dict] = None) -> T:
    ctx = context or {}
    attempt = 0
    last_err: Optional[Exception] = None

    while attempt < policy.max_attempts:
        attempt += 1
        try:
            logger.info("Ingestion attempt started", extra={"op": op_name, "attempt": attempt, **ctx})
            out = fn()
            logger.info("Ingestion attempt succeeded", extra={"op": op_name, "attempt": attempt, **ctx})
            return out
        except Exception as e:
            last_err = e
            logger.warning(
                "Ingestion attempt failed",
                extra={"op": op_name, "attempt": attempt, "error": str(e), **ctx},
            )

            if attempt >= policy.max_attempts:
                break

            delay = min(policy.base_delay_sec * (2 ** (attempt - 1)), policy.max_delay_sec)
            time.sleep(delay)

    assert last_err is not None
    logger.error("Ingestion failed after retries", extra={"op": op_name, "attempts": policy.max_attempts, **ctx})
    raise last_err
