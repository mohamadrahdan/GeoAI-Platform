from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pytest
from core.common.exceptions import ExecutionError
from core.config.loader import AppConfig
from core.data_manager.local_fs import LocalFileSystemDataManager
from core.inference.engine import InferenceContext, InferenceEngine
from core.inference.providers import InMemoryModelProvider
from core.inference.schemas import InferenceRequest
from core.logging.logger import get_module_logger
from core.models.artifacts import LocalArtifactStore
from core.models.base import BaseModel
from core.models.contracts import ModelInput, ModelOutput, SpatialMetadata
from core.models.metadata import ModelMetadata, ModelVersion
from core.models.registry import ModelRegistry

import time
from core.common.exceptions import InferenceTimeoutError

# Dummy model for testing
class DummyModel(BaseModel):
    def __init__(self) -> None:
        meta = ModelMetadata(
            name="dummy_model",
            task="test",
            framework="numpy",
            version=ModelVersion(1, 0, 0),
            schema_version="v1",
        )
        super().__init__(metadata=meta)

    def on_load(self) -> None:
        # No-op for tests
        return None

    def on_predict(self, x: ModelInput) -> ModelOutput:
        # Deterministic output: prediction filled with mean of input
        mean_val = float(np.mean(x.data))
        pred = np.full((1, x.data.shape[1], x.data.shape[2]), mean_val, dtype=np.float32)
        return ModelOutput(
            prediction=pred,
            spatial=x.spatial,
            confidence=None,
            extra={"dummy": True},
        )
    def predict(self, x: ModelInput) -> ModelOutput:
        # Keep predict delegating to the hook used by the base contract
        return self.on_predict(x)

# Fixtures
@pytest.fixture
def engine(tmp_path: Path) -> InferenceEngine:
    # Config (only for logger helper)
    cfg = AppConfig(env="test", data_root=tmp_path / "data", log_level="INFO")
    logger = get_module_logger("tests.inference", config=cfg)
    # Artifact store + registry
    store = LocalArtifactStore(root_dir=tmp_path / "artifacts")
    registry = ModelRegistry(artifact_store=store)
    # Provider (in-memory)
    provider = InMemoryModelProvider(registry=registry)
    # Register dummy model instance
    provider.register(DummyModel())
    # Data manager
    dm = LocalFileSystemDataManager(data_root=tmp_path / "data")
    ctx = InferenceContext(
        registry=registry,
        model_provider=provider,
        data_manager=dm,
        logger=logger,
    )
    return InferenceEngine(ctx)

# Test 1: input_payload
def test_execute_with_input_payload(engine: InferenceEngine) -> None:
    payload = {
        "data": np.ones((3, 4, 4), dtype=np.float32).tolist(),
        "bands": ["R", "G", "B"],
        "spatial": {"crs": "EPSG:4326", "bbox": [0, 0, 1, 1], "resolution": 10.0},
    }
    req = InferenceRequest(
        model_name="dummy_model",
        input_payload=payload,
    )
    resp = engine.execute(req)
    assert resp.model_name == "dummy_model"
    assert resp.version == "1.0.0"
    assert isinstance(resp.output, ModelOutput)
    assert resp.output.prediction.shape == (1, 4, 4)
    assert float(resp.output.prediction[0, 0, 0]) == 1.0
    assert "total" in resp.timings_ms

# Test 2: file://...json
def test_execute_with_file_uri(engine: InferenceEngine, tmp_path: Path) -> None:
    payload = {
        "data": np.zeros((3, 2, 2), dtype=np.float32).tolist(),
        "bands": ["R", "G", "B"],
        "spatial": {"crs": "EPSG:4326", "bbox": [0, 0, 1, 1], "resolution": 10.0},
    }
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps(payload), encoding="utf-8")
    req = InferenceRequest(
        model_name="dummy_model",
        input_uri=input_path.as_uri(),
    )
    resp = engine.execute(req)
    assert resp.output.prediction.shape == (1, 2, 2)
    assert float(resp.output.prediction[0, 0, 0]) == 0.0

# Test 3: model not found -> ExecutionError
def test_execute_model_not_found(tmp_path: Path) -> None:
    cfg = AppConfig(env="test", data_root=tmp_path / "data", log_level="INFO")
    logger = get_module_logger("tests.inference", config=cfg)
    store = LocalArtifactStore(root_dir=tmp_path / "artifacts")
    registry = ModelRegistry(artifact_store=store)
    provider = InMemoryModelProvider(registry=registry)
    dm = LocalFileSystemDataManager(data_root=tmp_path / "data")
    ctx = InferenceContext(
        registry=registry,
        model_provider=provider,
        data_manager=dm,
        logger=logger,
    )
    engine = InferenceEngine(ctx)
    payload = {
        "data": np.ones((3, 2, 2), dtype=np.float32).tolist(),
        "bands": ["R", "G", "B"],
        "spatial": {"crs": "EPSG:4326", "bbox": [0, 0, 1, 1], "resolution": 10.0},
    }
    req = InferenceRequest(
        model_name="unknown_model",
        input_payload=payload,
    )
    with pytest.raises(ExecutionError):
        engine.execute(req)




class SlowModel(DummyModel):
    def on_predict(self, x: ModelInput) -> ModelOutput:
        time.sleep(0.2)
        return super().on_predict(x)

def test_execute_timeout(engine: InferenceEngine, tmp_path: Path) -> None:
    # replace provider model with slow model
    engine._ctx.model_provider.register(SlowModel())

    payload = {
        "data": np.ones((3, 2, 2), dtype=np.float32).tolist(),
        "bands": ["R", "G", "B"],
        "spatial": {"crs": "EPSG:4326", "bbox": [0, 0, 1, 1], "resolution": 10.0},
    }
    req = InferenceRequest(
        model_name="dummy_model",
        input_payload=payload,
        parameters={"timeout_s": 0.05},
    )
    with pytest.raises(InferenceTimeoutError):
        engine.execute(req)

        

class FailingModel(DummyModel):
    def on_predict(self, x: ModelInput) -> ModelOutput:
        raise RuntimeError("boom")

def test_execute_predict_failure_wrapped(engine: InferenceEngine) -> None:
    engine._ctx.model_provider.register(FailingModel())

    payload = {
        "data": np.ones((3, 2, 2), dtype=np.float32).tolist(),
        "bands": ["R", "G", "B"],
        "spatial": {"crs": "EPSG:4326", "bbox": [0, 0, 1, 1], "resolution": 10.0},
    }
    req = InferenceRequest(model_name="dummy_model", input_payload=payload)
    with pytest.raises(ExecutionError):
        engine.execute(req)