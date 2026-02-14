from backend.services.models.base import BaseModel, ModelId

class DummyModel(BaseModel):

    def load(self) -> None:
        self._is_loaded = True

    def predict(self, inputs):
        if not self._is_loaded:
            raise RuntimeError("Model not loaded")
        return {"status": "ok"}

    def unload(self) -> None:
        self._is_loaded = False

def test_model_lifecycle():
    model = DummyModel(ModelId(name="dummy", version="0.1"))
    assert not model.is_loaded

    model.load()
    assert model.is_loaded

    result = model.predict({})
    assert result["status"] == "ok"

    model.unload()
    assert not model.is_loaded
