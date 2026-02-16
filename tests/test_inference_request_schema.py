import pytest
from core.inference.schemas import InferenceRequest, VersionSpec

def test_request_requires_some_input():
    req = InferenceRequest(model_name="unet")
    with pytest.raises(ValueError):
        req.validate_input()

def test_exact_version_requires_value():
    req = InferenceRequest(
        model_name="unet",
        version=VersionSpec(strategy="exact", value=None),
        input_uri="s3://bucket/x.tif"
    )
    with pytest.raises(ValueError):
        req.validate_input()

def test_latest_version_ok_and_input_ok():
    req = InferenceRequest(
        model_name="unet",
        input_uri="s3://bucket/x.tif"
    )
    req.validate_input()
