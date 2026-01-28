from __future__ import annotations
from typing import Generic, Iterable, Optional, Protocol, TypeVar

TEntity = TypeVar("TEntity")
TId = TypeVar("TId")

class BaseRepository(Protocol, Generic[TEntity, TId]):
    "Repository interface (storage abstraction)"

    def get(self, entity_id: TId) -> Optional[TEntity]: ...
    def list(self, limit: int = 100, offset: int = 0) -> Iterable[TEntity]: ...

    def add(self, entity: TEntity) -> TEntity: ...
    def delete(self, entity: TEntity) -> None: ...
