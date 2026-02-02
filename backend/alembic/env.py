from __future__ import annotations
import sys
from pathlib import Path
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# Make project root importable
# backend/alembic/env.py -> project root is two levels up
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Alembic config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import metadata
# IMPORTANT: import Base and models so metadata is populated
from backend.db.base import Base  # noqa: E402
from backend.db import models  # noqa: F401, E402
from backend.db.models import Dataset, Run, Result, Feedback  # noqa: F401

target_metadata = Base.metadata

def get_url() -> str:
    """
    Read DB URL for migrations.
    MVP approach: use DATABASE_URL env var.
    This avoids coupling Alembic to the full ServiceContainer bootstrap.
    """
    import os
    return os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://geoai:geoai@localhost:5432/geoai",
    )

def run_migrations_offline() -> None:
    "Run migrations in offline mode (no DBAPI needed)"
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_object=include_object,
    )
    with context.begin_transaction():
        context.run_migrations()

def include_object(object, name, type_, reflected, compare_to):
    # Ignore PostGIS / extension-managed tables
    if type_ == "table" and name in {"spatial_ref_sys", "topology", "layer"}:
        return False
    return True


def run_migrations_online() -> None:
    "Run migrations in online mode (engine + connection)"
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_object=include_object,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
