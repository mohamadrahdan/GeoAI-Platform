from __future__ import annotations
from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from core.models.contracts import ModelOutput


class TraceEvent(BaseModel):
    name: str
    ms: float
    ok: bool = True
    detail: Optional[str] = None
    
class VersionSpec(BaseModel):
    """
    Version resolution strategy for a model:
    - exact: use exact version string
    - latest: pick latest registered version
    """
    strategy: Literal["exact", "latest"] = Field(default="latest")
    value: Optional[str] = Field(default=None, description="Required when strategy=exact")

class InferenceRequest(BaseModel):
    "Standard inference request contract"
    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True,
    )
    request_id: Optional[str] = Field(default=None)
    trace_id: str = Field(..., min_length=8)
    model_name: str
    version: str
    output: ModelOutput
    timings_ms: Dict[str, float] = Field(default_factory=dict)
    events: List[TraceEvent] = Field(default_factory=list)
    tags: Dict[str, str] = Field(default_factory=dict)

class InferenceResponse(BaseModel):
    "Standard inference response contract"
    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True,
    )
    request_id: Optional[str] = Field(default=None)
    model_name: str
    version: str
    output: ModelOutput
    timings_ms: Dict[str, float] = Field(default_factory=dict)
    tags: Dict[str, str] = Field(default_factory=dict)
