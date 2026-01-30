from __future__ import annotations

from typing import Iterator
from db.uow import UnitOfWork

def get_uow() -> Iterator[UnitOfWork]:
    # Each request gets a fresh UoW + session, commits/rollbacks safely
    with UnitOfWork() as uow:
        yield uow
