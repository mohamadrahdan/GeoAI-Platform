from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class ResultCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str
    result_type: str = Field(min_length=1, max_length=100)
    uri: str = Field(min_length=1, max_length=4000)
    metrics: Optional[Dict[str, Any]] = None
    footprint_wkt: Optional[str] = None

class ResultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    run_id: str
    result_type: str
    uri: str
    metrics_json: Optional[Dict[str, Any]]
    footprint_wkt: Optional[str]
    created_at: datetime
