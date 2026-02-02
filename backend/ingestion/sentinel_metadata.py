from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Tuple
from backend.db.models import Run, Result
from backend.db.uow import UnitOfWork
from core.data_manager.base import BaseDataManager
from core.logging.logger import get_module_logger

from backend.ingestion.validators import (
    ensure_dict,
    extract_stac_datetime_iso,
    extract_stac_footprint_wkt,
)

logger = get_module_logger(__name__)

@dataclass(frozen=True)
class SentinelMetadataIngestionInput:
    dataset_id: str
    metadata: Dict[str, Any]          # already loaded JSON dict
    source_name: str = "sentinel"     # e.g., "sentinelhub" or "stac"
    item_id: Optional[str] = None

def ingest_sentinel_metadata(inp: SentinelMetadataIngestionInput, dm: BaseDataManager) -> str:
    """
    Stores raw metadata and registers a DB run/result.
    Returns run_id.
    """
    md = ensure_dict(inp.metadata)

    stac_dt = extract_stac_datetime_iso(md)  # may be None
    footprint_wkt = extract_stac_footprint_wkt(md)  # may be None

    with UnitOfWork() as uow:
        run = Run(
            dataset_id=inp.dataset_id,
            plugin_name="ingestion.sentinel_metadata",
            status="running",
            params_json={
                "source_name": inp.source_name,
                "item_id": inp.item_id or md.get("id"),
                "datetime": stac_dt,
            },
        )
        uow.runs.add(run)

        relpath = f"datasets/{inp.dataset_id}/sentinel/metadata_{run.id}.json"
        uri = dm.write_text(relpath, json.dumps(md, ensure_ascii=False, indent=2))

        res = Result(
            run_id=run.id,
            result_type="sentinel_metadata",
            uri=uri,
            metrics_json={"source_name": inp.source_name, "item_id": inp.item_id or md.get("id")},
            footprint_wkt=footprint_wkt,
        )
        uow.results.add(res)

        uow.runs.set_status(run.id, "done")

        logger.info(
            "Sentinel metadata ingestion completed",
            extra={"dataset_id": inp.dataset_id, "run_id": run.id, "item_id": inp.item_id or md.get("id")},
        )
        return run.id
