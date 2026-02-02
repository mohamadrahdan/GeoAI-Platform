from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from backend.db.models import Result
from backend.db.uow import UnitOfWork
from backend.api.deps import get_uow
from backend.api.schemas.results import ResultCreate, ResultOut

router = APIRouter(prefix="/results", tags=["results"])

@router.post("", response_model=ResultOut, status_code=status.HTTP_201_CREATED)
def persist_result(payload: ResultCreate, uow: UnitOfWork = Depends(get_uow)) -> ResultOut:
    run = uow.runs.get(payload.run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found.")

    res = Result(
        run_id=payload.run_id,
        result_type=payload.result_type,
        uri=payload.uri,
        metrics_json=payload.metrics,
        footprint_wkt=payload.footprint_wkt,
    )
    uow.results.add(res)
    return ResultOut.model_validate(res)


@router.get("/{result_id}", response_model=ResultOut)
def get_result(result_id: str, uow: UnitOfWork = Depends(get_uow)) -> ResultOut:
    res = uow.results.get(result_id)
    if not res:
        raise HTTPException(status_code=404, detail="Result not found.")
    return ResultOut.model_validate(res)

