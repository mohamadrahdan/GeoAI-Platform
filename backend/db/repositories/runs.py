from __future__ import annotations

from typing import Iterable, Optional
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from backend.db.models import Run

class RunRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, run_id: str) -> Optional[Run]:
        return self._session.get(Run, run_id)

    def list(self, limit: int = 100, offset: int = 0) -> Iterable[Run]:
        stmt = select(Run).order_by(Run.created_at.desc()).limit(limit).offset(offset)
        return self._session.scalars(stmt).all()

    def add(self, run: Run) -> Run:
        self._session.add(run)
        return run

    def delete(self, run: Run) -> None:
        self._session.delete(run)

    # Domain-specific
    def list_by_dataset(self, dataset_id: str, limit: int = 100, offset: int = 0) -> Iterable[Run]:
        stmt = (
            select(Run)
            .where(Run.dataset_id == dataset_id)
            .order_by(Run.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return self._session.scalars(stmt).all()

    def set_status(self, run_id: str, status: str) -> None:
        stmt = update(Run).where(Run.id == run_id).values(status=status)
        self._session.execute(stmt)
