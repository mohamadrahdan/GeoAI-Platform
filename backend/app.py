from fastapi import FastAPI

from core.services import get_container

def create_app() -> FastAPI:
    app = FastAPI(title="GeoAI-Platform", version="0.1.0")

    container = get_container()
    app.state.container = container

    return app
