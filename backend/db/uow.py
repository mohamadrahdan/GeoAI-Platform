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
    - owns a SQLAlchemy session per request/use-case
    - exposes repositories bound to that session
    - centralizes commit/rollback
    """

    def __init__(self) -> None:
        self.session: Optional[Session] = None

        # NOTE: Non-optional attributes; they are initialized in __enter__.
        self.datasets: DatasetRepository
        self.runs: RunRepository
        self.results: ResultRepository

    def __enter__(self) -> "UnitOfWork":
        self.session = SessionLocal()

        # Repositories are guaranteed to exist after entering the context
        self.datasets = DatasetRepository(self.session)
        self.runs = RunRepository(self.session)
        self.results = ResultRepository(self.session)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        assert self.session is not None

        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
