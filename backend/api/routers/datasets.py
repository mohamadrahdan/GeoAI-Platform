from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from db.models import Dataset
from db.uow import UnitOfWork
from api.deps import get_uow
from api.schemas.datasets import DatasetCreate, DatasetOut, DatasetUpdate

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.post("", response_model=DatasetOut, status_code=status.HTTP_201_CREATED)
def create_dataset(payload: DatasetCreate, uow: UnitOfWork = Depends(get_uow)) -> DatasetOut:
    # Prevent duplicates by name (simple MVP rule)
    existing = uow.datasets.get_by_name(payload.name)
    if existing:
        raise HTTPException(status_code=409, detail="Dataset with this name already exists.")

    ds = Dataset(name=payload.name, description=payload.description)
    uow.datasets.add(ds)
    return DatasetOut.model_validate(ds)


@router.get("/{dataset_id}", response_model=DatasetOut)
def get_dataset(dataset_id: str, uow: UnitOfWork = Depends(get_uow)) -> DatasetOut:
    ds = uow.datasets.get(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    return DatasetOut.model_validate(ds)


@router.get("", response_model=List[DatasetOut])
def list_datasets(
    limit: int = 100,
    offset: int = 0,
    uow: UnitOfWork = Depends(get_uow),
) -> List[DatasetOut]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    items = uow.datasets.list(limit=limit, offset=offset)
    return [DatasetOut.model_validate(x) for x in items]

@router.patch("/{dataset_id}", response_model=DatasetOut)
def update_dataset(
    dataset_id: str,
    payload: DatasetUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> DatasetOut:
    ds = uow.datasets.get(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    if payload.name is not None:
        ds.name = payload.name
    if payload.description is not None:
        ds.description = payload.description
    return DatasetOut.model_validate(ds)


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dataset(dataset_id: str, uow: UnitOfWork = Depends(get_uow)) -> None:
    ds = uow.datasets.get(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    uow.datasets.delete(ds)
    return None
