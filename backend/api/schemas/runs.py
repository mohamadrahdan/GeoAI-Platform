from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, Field, ConfigDict

class RunCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dataset_id: str
    plugin_name: str = Field(min_length=1, max_length=200)
    params: Dict[str, Any] = Field(default_factory=dict)

class RunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    dataset_id: str
    plugin_name: str
    status: str
    params_json: Dict[str, Any]
    created_at: datetime
