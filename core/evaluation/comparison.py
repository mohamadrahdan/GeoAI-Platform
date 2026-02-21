from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass(frozen=True)
class RunMetrics:
    "Represents evaluation results of a single run"
    trace_id: str
    model_name: str
    version: str
    metrics: Dict[str, float]

def compare_runs(
    runs: List[RunMetrics],
    metric_name: str,
    higher_is_better: bool = True,
) -> List[RunMetrics]:
    "Sort runs based on a specific metric./Returns sorted list (best first)"
    def key_fn(run: RunMetrics) -> float:
        return run.metrics.get(metric_name, float("-inf"))
    return sorted(
        runs,
        key=key_fn,
        reverse=higher_is_better,
    )

def best_run(
    runs: List[RunMetrics],
    metric_name: str,
    higher_is_better: bool = True,
) -> Optional[RunMetrics]:
    "Return the best run according to a metric"
    if not runs:
        return None
    sorted_runs = compare_runs(
        runs,
        metric_name=metric_name,
        higher_is_better=higher_is_better,
    )
    return sorted_runs[0]