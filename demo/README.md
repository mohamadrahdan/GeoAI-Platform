# Demo Input Package

This folder contains the input used by the platform demo.

The sample is intentionally small and synthetic. It is not a Sentinel-2 scene, a training dataset, or a real landslide detection input.

Its purpose is to provide a stable geospatial-like payload that can exercise the complete inference path without requiring a GPU, external data services, or model artifacts.

## Included file

### `sample_inference_request.json`

A ready-to-send request body for:

```text
POST /inference
```

The request uses the built-in `DummyModel` through the `model_adapter` plugin.

The input payload represents a small raster-like tile:

* 3 bands: `R`, `G`, `B`
* Shape: `3 x 4 x 4`
* CRS: `EPSG:4326`
* Bounding box: `[0, 0, 1, 1]`
* Resolution: `10.0`

The values are synthetic and only exist to validate the platform contract.

## What this demo verifies

Running this request verifies that the platform can:

* Accept and validate a structured inference request
* Dynamically load a runtime model class
* Resolve and register the model through the in-memory model provider
* Execute the request through the `model_adapter` plugin
* Run inference through `InferenceEngine`
* Return a structured response with output, timings, tags, and execution events

## Expected behavior

`DummyModel` produces a simple one-channel prediction mask filled with ones.

This is deliberate. The demo is designed to validate platform execution, not model accuracy.

## What this demo is not

This package is not intended to represent:

* A real satellite image
* A Sentinel API workflow
* A trained U-Net or DeepLab model
* A landslide detection benchmark
* The Padena research dataset

Real models can later be trained in Kaggle, cloud GPU environments, or research infrastructure and then integrated through the same model and plugin architecture.
