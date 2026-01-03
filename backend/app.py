from __future__ import annotations

from fastapi import FastAPI

from core.services import get_container
from backend.api.health import router as health_router

from backend.api.plugins import router as plugins_router


def create_app() -> FastAPI:
    app = FastAPI(title="GeoAI-Platform", version="0.1.0")

    # Initialize core container once and store it in app state
    container = get_container()
    app.state.container = container

    # Routers
    app.include_router(health_router, tags=["system"])
    
    # inside create_app()
    app.include_router(plugins_router, tags=["plugins"])

    container.logger.info("FastAPI app created and core container injected.")
    return app
