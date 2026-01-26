from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class DatasetContract:
    id: str
    name: str
    description: Optional[str]
    created_at: datetime

@dataclass(frozen=True)
class RunContract:
    id: str
    dataset_id: str
    plugin_name: str
    status: str  # e.g., "created", "running", "done", "failed"
    created_at: datetime
    params: Dict[str, Any]

@dataclass(frozen=True)
class ResultContract:
    id: str
    run_id: str
    result_type: str  # e.g., "mask", "vector", "metrics"
    uri: str          # file path / object storage uri
    created_at: datetime
    footprint_wkt: Optional[str] = None  # MVP: WKT; later: geometry column
    metrics: Optional[Dict[str, Any]] = None

@dataclass(frozen=True)
class FeedbackContract:
    id: str
    result_id: str
    corrected_label: str
    created_at: datetime
    comment: Optional[str] = None
