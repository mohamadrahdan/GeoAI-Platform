from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
def health(request: Request) -> dict:
    container = getattr(request.app.state, "container", None)
    return {
        "status": "ok",
        "core_loaded": container is not None,
    }
