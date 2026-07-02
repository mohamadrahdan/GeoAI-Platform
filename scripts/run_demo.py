from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMO_REQUEST_PATH = PROJECT_ROOT / "demo" / "sample_inference_request.json"

API_URL = os.getenv("DEMO_API_URL", "http://localhost:8000")
REQUEST_TIMEOUT_SECONDS = 20


def load_demo_request() -> dict[str, Any]:
    "Load the version-controlled demo request fixture"
    if not DEMO_REQUEST_PATH.exists():
        raise FileNotFoundError(
            f"Demo request file was not found: {DEMO_REQUEST_PATH}"
        )

    try:
        payload = json.loads(DEMO_REQUEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Demo request file contains invalid JSON: {DEMO_REQUEST_PATH}"
        ) from exc

    if not isinstance(payload, dict):
        raise RuntimeError("Demo request payload must be a JSON object")

    return payload


def api_request(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any]]:
    "Send an HTTP request using only Python's standard library"
    url = f"{API_URL}{path}"

    body = None
    headers = {"Accept": "application/json"}

    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(
        url=url,
        data=body,
        headers=headers,
        method=method,
    )

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            response_body = response.read().decode("utf-8")
            return response.status, json.loads(response_body)

    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"{method} {path} failed with HTTP {exc.code}: {error_body}"
        ) from exc

    except URLError as exc:
        raise RuntimeError(
            f"Could not reach the API at {API_URL}. "
            "Start the platform first with: docker compose --profile dev up -d --build"
        ) from exc


def check_health() -> None:
    "Confirm that the backend is reachable and core services are initialized"
    status_code, data = api_request("GET", "/health")

    if status_code != 200:
        raise RuntimeError(f"Health check failed: {data}")

    if data.get("status") != "ok" or not data.get("core_loaded"):
        raise RuntimeError(f"Platform is not ready for inference: {data}")


def check_model_adapter_plugin() -> None:
    "Confirm that automatic plugin discovery found model_adapter"
    status_code, data = api_request("GET", "/plugins")

    if status_code != 200:
        raise RuntimeError(f"Plugin registry check failed: {data}")

    plugins = data.get("plugins", [])

    if "model_adapter" not in plugins:
        raise RuntimeError(
            "Required plugin 'model_adapter' was not discovered. "
            f"Available plugins: {plugins}"
        )


def run_inference(payload: dict[str, Any]) -> dict[str, Any]:
    "Send the packaged demo request to the public inference endpoint"
    status_code, data = api_request(
        method="POST",
        path="/inference",
        payload=payload,
    )

    if status_code != 200:
        raise RuntimeError(f"Demo inference failed: {data}")

    if data.get("status") != "ok":
        raise RuntimeError(f"Unexpected demo status: {data}")

    if data.get("plugin") != "model_adapter":
        raise RuntimeError(
            f"Unexpected plugin in response: {data.get('plugin')}"
        )

    result = data.get("result")

    if not isinstance(result, dict):
        raise RuntimeError(f"Missing inference result in response: {data}")

    if "output" not in result:
        raise RuntimeError(f"Missing model output in response: {data}")

    return data


def prediction_shape(prediction: Any) -> str:
    "Return a safe human-readable shape for nested prediction arrays"
    if not isinstance(prediction, list) or not prediction:
        return "unknown"

    channels = len(prediction)

    if not isinstance(prediction[0], list) or not prediction[0]:
        return str(channels)

    rows = len(prediction[0])

    if not isinstance(prediction[0][0], list):
        return f"{channels} x {rows}"

    columns = len(prediction[0][0])

    return f"{channels} x {rows} x {columns}"


def print_demo_summary(response: dict[str, Any]) -> None:
    "Print a compact, human-readable summary of the execution"
    result = response["result"]
    output = result["output"]
    prediction = output.get("prediction", [])

    events = result.get("events", [])
    timings = result.get("timings_ms", {})

    print("\nGeoAI Platform demo completed successfully.\n")
    print(f"API endpoint: {API_URL}/inference")
    print(f"Plugin: {response.get('plugin')}")
    print(f"Model: {result.get('model_name')}")
    print(f"Resolved version: {result.get('version')}")
    print(f"Trace ID: {result.get('trace_id')}")
    print(f"Prediction shape: {prediction_shape(prediction)}")

    total_ms = timings.get("total")
    if isinstance(total_ms, (int, float)):
        print(f"Total inference time: {total_ms:.2f} ms")

    print("\nExecution stages:")

    for event in events:
        status = "OK" if event.get("ok") else "FAILED"
        duration = event.get("ms", 0)

        if not isinstance(duration, (int, float)):
            duration = 0

        print(f"- {event.get('name')}: {status} ({duration:.2f} ms)")

    print("\nThe demo validated the path:")
    print("API -> Plugin Registry -> model_adapter -> InferenceEngine -> JSON response")


def main() -> int:
    try:
        print("Starting GeoAI Platform reproducible demo...")

        check_health()
        check_model_adapter_plugin()

        payload = load_demo_request()
        response = run_inference(payload)

        print_demo_summary(response)
        return 0

    except Exception as exc:
        print(f"\nDemo failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
