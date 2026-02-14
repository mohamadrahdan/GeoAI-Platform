from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

@dataclass(frozen=True)
class SpatialMetadata:
    "Spatial reference for raster inputs/outputs"
    crs: str                    # e.g. "EPSG:4326"
    bbox: Tuple[float, float, float, float]  # (minx, miny, maxx, maxy)
    resolution: float           # pixel size

@dataclass(frozen=True)
class ModelInput:
    "Standardized input contract for all models"
    data: np.ndarray            # shape: (C, H, W)
    bands: List[str]            # e.g. ["B02", "B03", "B04", "B08"]
    spatial: SpatialMetadata
    extra: Optional[Dict[str, Any]] = None

@dataclass(frozen=True)
class ModelOutput:
    "Standardized output contract"
    prediction: np.ndarray      # shape: (1, H, W) or (classes, H, W)
    spatial: SpatialMetadata
    confidence: Optional[np.ndarray] = None
    extra: Optional[Dict[str, Any]] = None
