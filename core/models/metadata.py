from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class ModelVersion:
    """
    Semantic-ish versioning (major.minor.patch) with optional build tag.
    Stored knowing it will be compared/resolved later by the registry.
    """
    major: int
    minor: int
    patch: int
    build: Optional[str] = None

    def __str__(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return f"{base}+{self.build}" if self.build else base

@dataclass(frozen=True)
class ModelMetadata:
    """
    Model identity + reproducibility fields.
    Keep this stable; registry & inference logs will rely on it.
    """
    name: str                       # e.g. "unet_landslide"
    task: str                       # e.g. "segmentation"
    framework: str                  # e.g. "pytorch" / "tensorflow"
    version: ModelVersion           # model version
    schema_version: str             # I/O contract version, e.g. "v1"
    artifact_uri: Optional[str] = None  # e.g. "s3://.../model.pt" or "file://..."
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    extra: Dict[str, Any] = field(default_factory=dict)
