from __future__ import annotations

from typing import Iterable, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.db.models import Dataset

class DatasetRepository:
    "Dataset repository using SQLAlchemy Session"

    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, dataset_id: str) -> Optional[Dataset]:
        return self._session.get(Dataset, dataset_id)

    def list(self, limit: int = 100, offset: int = 0) -> Iterable[Dataset]:
        stmt = select(Dataset).order_by(Dataset.created_at.desc()).limit(limit).offset(offset)
        return self._session.scalars(stmt).all()

    # def add(self, dataset: Dataset) -> Dataset:
    #     self._session.add(dataset)
    #     return dataset
    
    def add(self, dataset: Dataset) -> Dataset:
        self._session.add(dataset)
        self._session.flush()
        self._session.refresh(dataset)
        return dataset

    def delete(self, dataset: Dataset) -> None:
        self._session.delete(dataset)

    # Domain-friendly helpers (optional)
    def get_by_name(self, name: str) -> Optional[Dataset]:
        stmt = select(Dataset).where(Dataset.name == name)
        return self._session.scalars(stmt).first()
