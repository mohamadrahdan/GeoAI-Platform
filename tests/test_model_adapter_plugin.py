from core.services import get_container
from core.plugins.discovery import discover_plugins
from core.plugins.executor import PluginExecutor

def main():
    container = get_container()
    assert container.plugin_registry is not None
    # IMPORTANT: use plugin_registry (not model registry)
    discover_plugins("plugins", container.plugin_registry)
    assert "model_adapter" in container.plugin_registry.list(), "model_adapter plugin not discovered"
    executor = PluginExecutor(
        registry=container.plugin_registry,
        logger=container.logger,
    )
    payload = {
        "model_class": "tests.test_inference_engine_execute.DummyModel",
        "request": {
            "model_name": "dummy_model",
            "version": {"strategy": "latest"},
            "input_payload": {
                "data": [
                    # C=3, H=2, W=2  (مثال کوچک)
                    [[1, 1], [1, 1]],  # band 1
                    [[1, 1], [1, 1]],  # band 2
                    [[1, 1], [1, 1]],  # band 3
                ],
                "bands": ["R", "G", "B"],
                "spatial": {"crs": "EPSG:4326", "bbox": [0, 0, 1, 1], "resolution": 10.0},
            },
            "parameters": {},
            "tags": {"source": "plugin-test"},
        },
    }
    result = executor.run("model_adapter", payload)

    assert "output" in result, "No output returned"
    assert result.get("model_name") == "dummy_model", "Unexpected model_name"
    print("ModelAdapterPlugin test passed.")

if __name__ == "__main__":
    main()