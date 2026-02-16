from core.models.version_resolver import VersionResolver
from core.models.metadata import ModelVersion

def test_resolve_exact():
    versions = {
        "1.0.0": ModelVersion(1, 0, 0),
        "1.1.0": ModelVersion(1, 1, 0),
    }

    result = VersionResolver.resolve_exact(versions, "1.0.0")
    assert result.minor == 0

def test_resolve_latest():
    versions = {
        "1.0.0": ModelVersion(1, 0, 0),
        "1.2.0": ModelVersion(1, 2, 0),
        "1.1.5": ModelVersion(1, 1, 5),
    }

    result = VersionResolver.resolve_latest(versions)
    assert result.minor == 2
