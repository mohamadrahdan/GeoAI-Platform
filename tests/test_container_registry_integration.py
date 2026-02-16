from pathlib import Path
from core.services import ServiceContainer
from core.models.artifacts import LocalArtifactStore

def test_registry_uses_local_artifact_store_root(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    container = ServiceContainer.build()

    store = container.registry.artifact_store
    assert isinstance(store, LocalArtifactStore) 

    assert store.root_dir.name == "artifacts"
    assert store.root_dir == Path(tmp_path) / "artifacts"
