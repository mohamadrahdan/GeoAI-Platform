from __future__ import annotations
import json
from dataclasses import asdict
from pathlib import Path
from typing import List
from core.evaluation.comparison import RunMetrics

class EvaluationStore:
    "Simple file-based persistence for evaluation results"
    def __init__(self, root_dir: Path) -> None:
        self._root = root_dir
    def save(self, run: RunMetrics) -> Path:
        "Persist evaluation results to JSON file"
        path = (
            self._root
            / "evaluations"
            / run.model_name
            / run.version
        )
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / f"{run.trace_id}.json"
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(asdict(run), f, indent=2)
        return file_path

    def load_all(self, model_name: str, version: str) -> List[RunMetrics]:
        "Load all persisted runs for a model/version"
        path = (
            self._root
            / "evaluations"
            / model_name
            / version
        )
        if not path.exists():
            return []
        runs = []
        for file in path.glob("*.json"):
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                runs.append(RunMetrics(**data))
        return runs