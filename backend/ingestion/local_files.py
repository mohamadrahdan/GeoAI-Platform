from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional
from backend.db.models import Dataset, Run, Result
from backend.db.uow import UnitOfWork
# Minimal protocol-like usage assumed: write_text(path, text) -> uri
from core.data_manager.base import BaseDataManager
from core.logging.logger import get_module_logger

logger = get_module_logger(__name__)

@dataclass(frozen=True)
class LocalIngestionInput:
    dataset_name: str
    source_dir: Path
    description: Optional[str] = None
    glob_pattern: str = "*"

def _scan_files(source_dir: Path, glob_pattern: str) -> List[str]:
    files = [str(p) for p in source_dir.rglob(glob_pattern) if p.is_file()]
    return sorted(files)

def ingest_local_files(inp: LocalIngestionInput, dm: BaseDataManager) -> str:
    """
    Creates:
      -> Dataset
      -> Run(plugin=ingestion.local_files)
      -> Result(type=manifest) storing a manifest.json URI
    Returns dataset_id.
    """
    if not inp.source_dir.exists() or not inp.source_dir.is_dir():
        raise ValueError(f"source_dir not found or not a directory: {inp.source_dir}")

    files = _scan_files(inp.source_dir, inp.glob_pattern)
    if not files:
        raise ValueError(f"No files found in {inp.source_dir} using pattern {inp.glob_pattern}")

    with UnitOfWork() as uow:
        ds = Dataset(name=inp.dataset_name, description=inp.description)
        uow.datasets.add(ds)

        run = Run(
            dataset_id=ds.id,
            plugin_name="ingestion.local_files",
            status="running",
            params_json={
                "source_dir": str(inp.source_dir),
                "glob_pattern": inp.glob_pattern,
                "file_count": len(files),
            },
        )
        uow.runs.add(run)

        manifest = {
            "dataset_id": ds.id,
            "dataset_name": inp.dataset_name,
            "source_dir": str(inp.source_dir),
            "glob_pattern": inp.glob_pattern,
            "files": files,
        }

        # Store manifest under a stable path in the data manager
        manifest_relpath = f"datasets/{ds.id}/manifest.json"
        manifest_uri = dm.write_text(manifest_relpath, json.dumps(manifest, ensure_ascii=False, indent=2))

        res = Result(
            run_id=run.id,
            result_type="manifest",
            uri=manifest_uri,
            metrics_json={"file_count": len(files)},
            footprint_wkt=None,
        )
        uow.results.add(res)

        # Mark run done
        uow.runs.set_status(run.id, "done")

        logger.info("Local ingestion completed", extra={"dataset_id": ds.id, "run_id": run.id, "files": len(files)})

        return ds.id
