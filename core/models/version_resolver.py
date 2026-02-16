from __future__ import annotations
from typing import Dict
from core.models.metadata import ModelVersion

class VersionResolver:
    "Resolves model versions (exact, latest)"
    @staticmethod
    def resolve_exact(
        versions: Dict[str, ModelVersion],
        version: str,
    ) -> ModelVersion:
        if version not in versions:
            raise ValueError(f"Version not found: {version}")
        return versions[version]

    @staticmethod
    def resolve_latest(
        versions: Dict[str, ModelVersion],
    ) -> ModelVersion:
        if not versions:
            raise ValueError("No versions available.")

        sorted_versions = sorted(
            versions.values(),
            key=lambda v: (v.major, v.minor, v.patch),
        )

        return sorted_versions[-1]
