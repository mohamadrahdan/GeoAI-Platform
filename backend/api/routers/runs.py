from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from backend.db.models import Run
from backend.db.uow import UnitOfWork
from backend.api.schemas.runs import RunCreate, RunOut
from backend.api.deps import get_uow
from backend.api.schemas.datasets import DatasetOut
from backend.db.models import Dataset


router = APIRouter(prefix="/runs", tags=["runs"])

@router.post("", response_model=RunOut, status_code=status.HTTP_201_CREATED)
def register_run(payload: RunCreate, uow: UnitOfWork = Depends(get_uow)) -> RunOut:
    # Ensure dataset exists
    ds = uow.datasets.get(payload.dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    run = Run(
        dataset_id=payload.dataset_id,
        plugin_name=payload.plugin_name,
        status="created",
        params_json=payload.params,
    )
    uow.runs.add(run)
    return RunOut.model_validate(run)

@router.get("/{run_id}", response_model=RunOut)
def get_run(run_id: str, uow: UnitOfWork = Depends(get_uow)) -> RunOut:
    run = uow.runs.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found.")
    return RunOut.model_validate(run)
