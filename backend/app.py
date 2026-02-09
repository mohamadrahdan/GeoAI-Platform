from __future__ import annotations

from fastapi import FastAPI
from core.services import get_container
from backend.api.health import router as health_router
from backend.api.plugins import router as plugins_router
from backend.api.run import router as run_router
from backend.api.routers.datasets import router as datasets_router
from backend.api.routers.runs import router as runs_router
from backend.api.routers.results import router as results_router
from backend.api.routers.query import router as query_router


def create_app() -> FastAPI:
    app = create_app()
    
    app = FastAPI(title="GeoAI-Platform", version="0.1.0")

    # Initialize core container once and store it in app state
    container = get_container()
    app.state.container = container

    # Routers
    app.include_router(health_router, tags=["system"])

    # inside create_app()
    app.include_router(plugins_router, tags=["plugins"])

    # inside create_app()
    app.include_router(run_router, tags=["plugins"])

    app.include_router(datasets_router)

    app.include_router(runs_router)

    app.include_router(results_router)

    app.include_router(query_router)


    container.logger.info("FastAPI app created and core container injected.")
    return app

app = create_app()
