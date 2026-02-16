from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, Literal

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
    model_name: str = Field(..., min_length=1)
    version: VersionSpec = Field(default_factory=VersionSpec)

    # Input contract (generic)
    input_uri: Optional[str] = Field(
        default=None,
        description="URI/path to input data (file, tile set, etc.)")
    
    input_payload: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Inline input payload (e.g., small arrays/metadata)")

    # Optional execution parameters
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Runtime params like tile_size, bands, normalization, thresholds")

    # Optional tracing metadata
    request_id: Optional[str] = Field(default=None)
    tags: Dict[str, str] = Field(default_factory=dict)

    def validate_input(self) -> None:
        # At least one of input_uri or input_payload must be provided
        if self.input_uri is None and self.input_payload is None:
            raise ValueError("Either input_uri or input_payload must be provided.")
        # If exact, value must exist
        if self.version.strategy == "exact" and not self.version.value:
            raise ValueError("version.value is required when version.strategy='exact'.")
