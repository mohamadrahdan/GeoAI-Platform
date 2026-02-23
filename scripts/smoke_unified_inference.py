import os
import sys
import requests

API_URL = os.getenv("SMOKE_API_URL", "http://localhost:8000")

def main() -> int:
    body = {
        "model_class": "plugins.model_adapter.dummy_model.DummyModel",
        "timeout_seconds": 10,
        "request": {
            "model_name": "dummy_model",
            "version": {"strategy": "latest", "value": None},
            "input_payload": {
                "data": [
                    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
                    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
                    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
                ],
                "bands": ["R", "G", "B"],
                "spatial": {"crs": "EPSG:4326", "bbox": [0, 0, 1, 1], "resolution": 10.0},
            },
            "parameters": {},
            "request_id": None,
            "tags": {"source": "smoke-unified"},
        },
    }

    r = requests.post(f"{API_URL}/inference", json=body, timeout=15)
    if r.status_code != 200:
        raise RuntimeError(f"Unified inference failed: {r.status_code} {r.text}")
    data = r.json()
    result = data.get("result", {})
    if "output" not in result:
        raise RuntimeError(f"No output returned. Response: {data}")
    print("Smoke unified inference passed: /inference OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())