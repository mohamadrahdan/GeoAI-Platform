from __future__ import annotations

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from backend.db.uow import UnitOfWork
from backend.api.deps import get_uow
from backend.api.schemas.runs import RunOut
from backend.api.schemas.results import ResultOut

router = APIRouter(tags=["query"])

@router.get("/datasets/{dataset_id}/runs", response_model=List[RunOut])
def list_runs_for_dataset(
    dataset_id: str,
    limit: int = 100,
    offset: int = 0,
    uow: UnitOfWork = Depends(get_uow),
) -> List[RunOut]:
    ds = uow.datasets.get(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    limit = max(1, min(limit, 500))
    offset = max(0, offset)

    runs = uow.runs.list_by_dataset(dataset_id, limit=limit, offset=offset)
    return [RunOut.model_validate(r) for r in runs]

@router.get("/runs/{run_id}/results", response_model=List[ResultOut])
def list_results_for_run(
    run_id: str,
    limit: int = 200,
    offset: int = 0,
    uow: UnitOfWork = Depends(get_uow),
) -> List[ResultOut]:
    run = uow.runs.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found.")

    limit = max(1, min(limit, 1000))
    offset = max(0, offset)

    results = uow.results.list_by_run(run_id, limit=limit, offset=offset)
    return [ResultOut.model_validate(x) for x in results]

@router.get("/runs", response_model=List[RunOut])
def query_runs(
    dataset_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    uow: UnitOfWork = Depends(get_uow),
) -> List[RunOut]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)

    if dataset_id:
        runs = uow.runs.list_by_dataset(dataset_id, limit=limit, offset=offset)
    else:
        runs = uow.runs.list(limit=limit, offset=offset)

    return [RunOut.model_validate(r) for r in runs]

@router.get("/results", response_model=List[ResultOut])
def query_results(
    run_id: Optional[str] = None,
    result_type: Optional[str] = None,
    limit: int = 200,
    offset: int = 0,
    uow: UnitOfWork = Depends(get_uow),
) -> List[ResultOut]:
    limit = max(1, min(limit, 1000))
    offset = max(0, offset)

    # MVP: if both provided, return at most one match as a list
    if run_id and result_type:
        one = uow.results.get_by_run_and_type(run_id, result_type)
        return [ResultOut.model_validate(one)] if one else []

    if run_id:
        results = uow.results.list_by_run(run_id, limit=limit, offset=offset)
    else:
        results = uow.results.list(limit=limit, offset=offset)

    return [ResultOut.model_validate(x) for x in results]
