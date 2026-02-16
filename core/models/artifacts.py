from __future__ import annotations 
from dataclasses import dataclass 
from pathlib import Path 
from typing import Protocol, runtime_checkable 
import shutil 

@dataclass(frozen=True)
class ArtifactRef:
    model_name: str
    version: str
    filename: str

    def relpath(self) -> Path:
        return Path(self.model_name) / self.version / self.filename

@runtime_checkable
class ArtifactStore(Protocol):
    def put(self, ref: ArtifactRef, src_path: Path) -> Path: 
        "Store an artifact file and return the final stored path"
        ...
    def get(self, ref: ArtifactRef) -> Path:
        "Return the stored path for an artifact; raise FileNotFoundError if missing"
        ...
    def exists(self, ref: ArtifactRef) -> bool:
        "Check artifact existence"
        ...

@dataclass
class LocalArtifactStore:
    def __init__(self, root_dir: Path) -> None:
        self._root_dir = root_dir.resolve()

    @property
    def root_dir(self) -> Path:
        return self._root_dir

    def put(self, ref: ArtifactRef, src_path: Path) -> Path:
        if not src_path.exists():
            raise FileNotFoundError(f"Source artifact not found: {src_path}")

        dst = self.root_dir / ref.relpath()
        dst.parent.mkdir(parents=True, exist_ok=True)

        # Copy (preserve metadata); overwrite is allowed for idempotency in dev.
        shutil.copy2(src_path, dst)
        return dst

    def get(self, ref: ArtifactRef) -> Path:
        dst = self.root_dir / ref.relpath()
        if not dst.exists():
            raise FileNotFoundError(f"Artifact not found: {dst}")
        return dst

    def exists(self, ref: ArtifactRef) -> bool:
        return (self.root_dir / ref.relpath()).exists()

