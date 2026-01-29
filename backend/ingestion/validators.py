from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime
from shapely.geometry import shape
from shapely.wkt import dumps as wkt_dumps


class MetadataValidationError(ValueError):
    pass


def ensure_dict(obj: Any) -> Dict[str, Any]:
    if not isinstance(obj, dict):
        raise MetadataValidationError("metadata must be a dict")
    return obj

def extract_stac_datetime_iso(md: Dict[str, Any]) -> Optional[str]:
    # STAC usually: md["properties"]["datetime"]
    props = md.get("properties") or {}
    dt = props.get("datetime") or md.get("datetime")
    if not dt:
        return None
    # keep it as ISO string; validation can be stricter later
    return str(dt)

def extract_stac_footprint_wkt(md: Dict[str, Any]) -> Optional[str]:
    """
    Extract footprint from:
      -> md["geometry"] (GeoJSON)
    Returns WKT string (MVP).
    """
    geom = md.get("geometry")
    if not geom:
        return None

    try:
        shp = shape(geom)
        return wkt_dumps(shp, rounding_precision=7)
    except Exception as e:
        raise MetadataValidationError(f"invalid geometry in metadata: {e}") from e
