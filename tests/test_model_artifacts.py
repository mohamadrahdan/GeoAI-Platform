from __future__ import annotations
from pathlib import Path
import tempfile
from core.models.artifacts import LocalArtifactStore, ArtifactRef
from core.models.metadata import ModelMetadata, ModelVersion
from core.models.registry import ModelRegistry

def test_local_artifact_store_put_get_roundtrip() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "artifacts"
        store = LocalArtifactStore(root_dir=root)

        # Create a fake artifact
        src = Path(tmp) / "weights.bin"
        src.write_bytes(b"dummy-weights")

        ref = ArtifactRef(model_name="landslide_unet", version="1.0.0", filename="weights.bin")
        dst = store.put(ref, src)

        assert dst.exists()
        assert store.exists(ref) is True
        assert store.get(ref).read_bytes() == b"dummy-weights"

def test_registry_store_and_resolve_artifact() -> None: 
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "artifacts"
        store = LocalArtifactStore(root_dir=root)
        reg = ModelRegistry(artifact_store=store)

        meta = ModelMetadata(
            name="landslide_unet",
            task="segmentation",
            framework="pytorch",
            version=ModelVersion(1, 0, 0),
            schema_version="v1",
        )
        reg.register_model(meta)

        reg.add_version(
            "landslide_unet",
            ModelVersion(1, 0, 0),
        )

        src = Path(tmp) / "weights.bin"
        src.write_bytes(b"abc")

        reg.store_artifact("landslide_unet", "1.0.0", "weights.bin", src)
        resolved = reg.resolve_artifact("landslide_unet", "1.0.0", "weights.bin")

        assert resolved.exists()
        assert resolved.read_bytes() == b"abc"
