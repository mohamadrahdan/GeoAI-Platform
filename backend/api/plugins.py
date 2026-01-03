from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/plugins")
def list_plugins(request: Request) -> dict:
    container = request.app.state.container
    registry = container.plugin_registry
    return {
        "plugins": registry.list(),
    }
