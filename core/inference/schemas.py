from __future__ import annotations
from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from core.models.contracts import ModelOutput

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
    model_config = ConfigDict(protected_namespaces=())
    model_name: str = Field(..., min_length=1)
    version: VersionSpec = Field(default_factory=VersionSpec)
    input_uri: Optional[str] = Field(
        default=None,
        description="URI/path to input data (file://... or relative path under data_root)",
    )
    input_payload: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Inline input payload (e.g., small arrays/metadata)",
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Runtime params like tile_size, bands, normalization, thresholds",
    )
    request_id: Optional[str] = Field(default=None)
    tags: Dict[str, str] = Field(default_factory=dict)
    def validate_input(self) -> None:
        if self.input_uri is None and self.input_payload is None:
            raise ValueError("Either input_uri or input_payload must be provided.")
        if self.version.strategy == "exact" and not self.version.value:
            raise ValueError("version.value is required when version.strategy='exact'.")

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
