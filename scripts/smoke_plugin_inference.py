import os
import sys
import requests

API_URL = os.getenv("SMOKE_API_URL", "http://localhost:8000")
def main() -> int:
    payload = {
        "payload": {
            "model_class": "plugins.model_adapter.dummy_model.DummyModel",
            "request": {
                "model_name": "dummy_model",
                "version": {"strategy": "latest"},
                "input_payload": {
                    # C=3, H=4, W=4
                    "data": [
                        [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
                        [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
                        [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
                    ],
                    "bands": ["R", "G", "B"],
                    "spatial": {
                        "crs": "EPSG:4326",
                        "bbox": [0, 0, 1, 1],
                        "resolution": 10.0,
                    },
                },
                "parameters": {},
                "tags": {"source": "smoke-plugin"},
            },
        },
        "timeout_seconds": 10,
    }
    
    r = requests.post(f"{API_URL}/run/model_adapter", json=payload, timeout=15)
    if r.status_code != 200:
        raise RuntimeError(f"Plugin inference failed: {r.status_code} {r.text}")
    data = r.json()
    result = data.get("result", {})
    out = result.get("output")
    if out is None:
        raise RuntimeError("No output returned from plugin inference")
    print("Smoke plugin inference passed: /run/model_adapter OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())