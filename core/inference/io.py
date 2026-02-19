from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict
from urllib.parse import urlparse
import numpy as np
from core.common.exceptions import DataAccessError
from core.data_manager.base import BaseDataManager
from core.models.contracts import ModelInput, SpatialMetadata
from core.inference.schemas import InferenceRequest
from urllib.request import url2pathname


def load_input_from_request(req: InferenceRequest, data_manager: BaseDataManager) -> ModelInput:
    "Load/convert the request input into a standardized ModelInput"
    if req.input_payload is not None:
        return payload_to_model_input(req.input_payload)

    if req.input_uri is None:
        raise DataAccessError("No input_uri provided.")

    payload = load_payload_from_uri(req.input_uri, data_manager=data_manager)
    return payload_to_model_input(payload)

def load_payload_from_uri(uri: str, data_manager: BaseDataManager) -> Dict[str, Any]:
    "Load a JSON payload from either file:// or a relative path under data_root"
    parsed = urlparse(uri)

    # absolute path
    if parsed.scheme == "file":
        # Windows-safe conversion: file:///C:/... -> C:\...
        raw_path = url2pathname(parsed.path)
        # On Windows, urlparse gives "/C:/..." so remove the leading slash
        if raw_path.startswith("\\") and len(raw_path) > 3 and raw_path[2] == ":":
            raw_path = raw_path.lstrip("\\")
        path = Path(raw_path)
        if not path.exists():
            raise DataAccessError(f"Input file not found: {path}")
        if path.suffix.lower() != ".json":
            raise DataAccessError(f"Only JSON inputs are supported for file:// URIs (got: {path.suffix})")
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            raise DataAccessError(f"Failed to parse JSON input file: {path}") from e

    # No scheme -> treat as relative path in data_root
    if parsed.scheme == "":
        rel = uri
        if not data_manager.exists(rel):
            raise DataAccessError(f"Input not found under data_root: {rel}")
        data = data_manager.load(rel)
        if not isinstance(data, dict):
            raise DataAccessError(f"Expected JSON object at {rel}, got: {type(data).__name__}")
        return data
    raise DataAccessError(f"Unsupported input_uri scheme: {parsed.scheme}")

def payload_to_model_input(payload: Dict[str, Any]) -> ModelInput:
    "Convert a JSON-like payload into ModelInput"
    try:
        data = np.asarray(payload["data"], dtype=np.float32)
        bands = list(payload["bands"])
        spatial_raw = payload["spatial"]
        spatial = SpatialMetadata(
            crs=str(spatial_raw["crs"]),
            bbox=tuple(spatial_raw["bbox"]),
            resolution=float(spatial_raw["resolution"]),
        )
        extra = payload.get("extra")
    except KeyError as e:
        raise DataAccessError(f"Missing required payload field: {e}") from e
    except Exception as e:
        raise DataAccessError("Invalid input payload structure.") from e

    # Expect data shaped (C, H, W); accept (H, W, C) and transpose
    if data.ndim == 3 and data.shape[0] != len(bands) and data.shape[-1] == len(bands):
        data = np.transpose(data, (2, 0, 1))
    if data.ndim != 3:
        raise DataAccessError(f"Input data must be 3D (C,H,W); got shape={data.shape}")
    return ModelInput(data=data, bands=bands, spatial=spatial, extra=extra)
