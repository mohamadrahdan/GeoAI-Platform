from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Optional
from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.repositories.datasets import DatasetRepository
from db.repositories.runs import RunRepository
from db.repositories.results import ResultRepository

class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    """
    Unit of Work:
    -> owns a SQLAlchemy session
    -> exposes repositories bound to that session
    -> controls commit/rollback
    """

    def __init__(self) -> None:
        self.session: Optional[Session] = None
        # Repositories (initialized in __enter__)
        self.datasets: Optional[DatasetRepository] = None
        self.runs: Optional[RunRepository] = None
        self.results: Optional[ResultRepository] = None

    def __enter__(self) -> "UnitOfWork":
        self.session = SessionLocal()
        self.datasets = DatasetRepository(self.session)
        self.runs = RunRepository(self.session)
        self.results = ResultRepository(self.session)
        return self

    def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork has no active session.")
        self.session.commit()

    def rollback(self) -> None:
        if self.session is None:
            return
        self.session.rollback()

    def __exit__(self, exc_type, exc, tb) -> None:
        assert self.session is not None

        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
