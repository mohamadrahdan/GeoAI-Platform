import numpy as np
from core.models.contracts import ModelInput, ModelOutput, SpatialMetadata

def test_model_input_output_contract():
    spatial = SpatialMetadata(
        crs="EPSG:4326",
        bbox=(0.0, 0.0, 1.0, 1.0),
        resolution=10.0,
    )

    dummy_input = ModelInput(
        data=np.zeros((4, 256, 256)),
        bands=["B02", "B03", "B04", "B08"],
        spatial=spatial,
    )

    dummy_output = ModelOutput(
        prediction=np.zeros((1, 256, 256)),
        spatial=spatial,
    )

    assert dummy_input.data.shape == (4, 256, 256)
    assert dummy_output.prediction.shape == (1, 256, 256)
    assert dummy_input.spatial.crs == "EPSG:4326"
