from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.config.settings import load_database_settings

def create_db_engine():
    settings = load_database_settings()
    # pool_pre_ping avoids stale connections in long-running services
    return create_engine(settings.url, pool_pre_ping=True, future=True)

_ENGINE = create_db_engine()

SessionLocal = sessionmaker(
    bind=_ENGINE,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)

@contextmanager
def db_session() -> Iterator[Session]:
    "Context-managed DB session"
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
