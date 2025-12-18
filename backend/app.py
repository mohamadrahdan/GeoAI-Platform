from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(title="GeoAI-Platform", version="0.1.0")
    return app
