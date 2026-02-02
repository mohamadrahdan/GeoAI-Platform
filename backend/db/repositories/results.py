from __future__ import annotations

from typing import Iterable, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.db.models import Result

class ResultRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, result_id: str) -> Optional[Result]:
        return self._session.get(Result, result_id)

    def list(self, limit: int = 100, offset: int = 0) -> Iterable[Result]:
        stmt = select(Result).order_by(Result.created_at.desc()).limit(limit).offset(offset)
        return self._session.scalars(stmt).all()

    def add(self, result: Result) -> Result:
        self._session.add(result)
        return result

    def delete(self, result: Result) -> None:
        self._session.delete(result)

    # Domain-specific
    def list_by_run(self, run_id: str, limit: int = 200, offset: int = 0) -> Iterable[Result]:
        stmt = (
            select(Result)
            .where(Result.run_id == run_id)
            .order_by(Result.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return self._session.scalars(stmt).all()

    def get_by_run_and_type(self, run_id: str, result_type: str) -> Optional[Result]:
        stmt = select(Result).where(Result.run_id == run_id, Result.result_type == result_type)
        return self._session.scalars(stmt).first()
