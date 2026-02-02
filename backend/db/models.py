from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, Optional, List
from sqlalchemy import (String, DateTime, ForeignKey, Text, Index,)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.db.base import Base
from geoalchemy2 import Geometry


def new_id() -> str:
    return str(uuid.uuid4())

class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    runs: Mapped[List["Run"]] = relationship(
        back_populates="dataset",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

class Run(Base):
    __tablename__ = "runs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    dataset_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
    )
    plugin_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="created")
    params_json: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    dataset: Mapped["Dataset"] = relationship(back_populates="runs")

    results: Mapped[List["Result"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("idx_runs_dataset_id", "dataset_id"),
        Index("idx_runs_status", "status"),
    )

class Result(Base):
    __tablename__ = "results"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    run_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("runs.id", ondelete="CASCADE"),
        nullable=False,
    )
    result_type: Mapped[str] = mapped_column(String, nullable=False)
    uri: Mapped[str] = mapped_column(Text, nullable=False)
    metrics_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    footprint_wkt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    footprint_geom: Mapped[Optional[Any]] = mapped_column(
        Geometry(geometry_type="GEOMETRY", srid=4326),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    run: Mapped["Run"] = relationship(back_populates="results")

    feedback_items: Mapped[List["Feedback"]] = relationship(
        back_populates="result",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("idx_results_run_id", "run_id"),
        Index("idx_results_type", "result_type"),
        Index("idx_results_geom", "footprint_geom", postgresql_using="gist"),
    )


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    result_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("results.id", ondelete="CASCADE"),
        nullable=False,
    )
    corrected_label: Mapped[str] = mapped_column(String, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    result: Mapped["Result"] = relationship(back_populates="feedback_items")

    __table_args__ = (
        Index("idx_feedback_result_id", "result_id"),
    )
