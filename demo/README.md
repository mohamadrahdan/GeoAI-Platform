# Demo Input Package

This folder contains the small reproducible demo input used by GeoAI Platform.

The demo is intentionally lightweight. It does not use real Sentinel imagery, a GeoTIFF file, a trained landslide model, or a scientific benchmark dataset.

Its purpose is to verify that the platform can execute an inference request through the real backend path:

```text
API
→ Plugin Registry
→ model_adapter
→ InferenceEngine
→ JSON response
```

The demo validates the platform workflow, not model accuracy.

---

## Files

```text
demo/
  sample_inference_request.json
  README.md
```

The main file is:

```text
sample_inference_request.json
```

It contains a version-controlled inference request that can be sent to the backend through:

```text
scripts/run_demo.py
```

---

## What the sample request contains

The demo request includes:

```text
model_class
timeout_seconds
model name
version strategy
input payload
spatial metadata
request tags
```

The input payload is a small synthetic three-band raster-like array.

It is deliberately small so the demo can run quickly on a normal local machine without GPU support or external data services.

The input is not:

```text
a real satellite image
a Sentinel-2 scene
a GeoTIFF
a landslide dataset
a validation benchmark
```

---

## Demo model

The request uses a lightweight demo model:

```text
DummyModel
```

`DummyModel` exists only to confirm that the platform can load a model implementation, run the inference lifecycle, and return a structured response.

It should not be interpreted as a real GeoAI model.

A future landslide-detection workflow would replace this demo model with a trained model package, such as a U-Net or DeepLab-based segmentation model.

---

## Run the demo

From the repository root, create a local environment file:

```bash
cp .env.example .env
```

Then fill in the required database values in `.env`:

```text
POSTGRES_USER
POSTGRES_PASSWORD
```

Start the local development stack:

```bash
docker compose --profile dev up -d --build
```

Run the demo script:

```bash
python scripts/run_demo.py
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

After filling in the required values in `.env`:

```powershell
docker compose --profile dev up -d --build
python scripts/run_demo.py
```

---

## What the demo script checks

The demo runner performs these checks:

```text
1. The backend is reachable.
2. The health endpoint returns a successful status.
3. The core application container is loaded.
4. The plugin list is available.
5. model_adapter has been discovered.
6. The sample request can be loaded from this folder.
7. POST /inference returns a successful response.
8. The response contains the expected plugin, model, trace, timing, and output information.
```

This gives a quick way to verify that the main platform path works after a fresh local setup.

---

## Expected output

The exact trace ID and timing values will change between runs.

A successful run should look conceptually like this:

```text
Starting GeoAI Platform reproducible demo...

GeoAI Platform demo completed successfully.

API endpoint: http://localhost:8000/inference
Plugin: model_adapter
Model: dummy_model
Resolved version: 1.0.0
Trace ID: <generated-trace-id>
Prediction shape: 1 x 4 x 4
Total inference time: <value> ms

Execution stages:
- validate: OK
- resolve_version: OK
- load_model: OK
- load_input: OK
- predict: OK

The demo validated the path:
API -> Plugin Registry -> model_adapter -> InferenceEngine -> JSON response
```

The exact timing is not important.

The important point is that the expected stages complete successfully and the request moves through the intended platform architecture.

---

## Relationship to the main documentation

This folder explains the runnable demo input.

For a broader explanation of the demo pipeline, see:

```text
docs/demo-pipeline.md
```

For the inference lifecycle, see:

```text
docs/inference-lifecycle.md
```

For the plugin execution path, see:

```text
docs/plugin-flow.md
```

---

## Current scope

This demo package is part of the public portfolio release preparation.

It is designed to make the project locally verifiable without requiring heavy data, trained model artifacts, GPU access, or external geospatial services.

Future versions can replace the synthetic payload and `DummyModel` with a real model package and real raster input, while keeping the same basic platform path.