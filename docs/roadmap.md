# Roadmap

## Purpose

This roadmap describes the current direction of GeoAI Platform after the initial platform foundation has been built.

The project is no longer at the early repository-setup stage. It now includes a working backend, plugin execution, model inference foundation, PostGIS persistence, a reproducible demo, public-facing documentation, and an early frontend workspace.

The next work is not about rebuilding the system from scratch.

The next work is about connecting this foundation to real geospatial data, real trained models, stronger frontend interaction, and more production-oriented workflows.

This roadmap is intentionally practical. It separates what already exists from what should come next.

---

## Current foundation

The platform currently provides:

```text
FastAPI backend
PostgreSQL / PostGIS persistence
Docker-based local development stack
Alembic migrations
Plugin discovery and registry
Generic plugin execution
model_adapter inference plugin
InferenceEngine lifecycle
Model registry and version resolution
Local data manager abstraction
Dataset, Run, Result and Feedback persistence
Structured middleware and request metrics
Reproducible DummyModel demo
Early React / TypeScript frontend workspace
Public architecture and demo documentation
```

This foundation is enough to demonstrate the platform architecture and verify the main execution path locally.

It is not yet a complete GeoAI product with real satellite-model inference.

---

## Roadmap principle

The guiding principle is:

> Keep the platform stable while adding real GeoAI capability through clear contracts.

Future work should not move model-specific or workflow-specific logic directly into the API layer.

Instead, new capabilities should be added through:

```text
plugin contracts
model contracts
data input contracts
preprocessing contracts
result persistence contracts
frontend interaction contracts
```

This keeps the platform easier to understand, test, and extend.

---

## Near-term roadmap

### 1. Final public release preparation

The first priority is to make the current repository clean, inspectable, and easy to evaluate.

This includes:

```text
final README alignment
architecture documentation cleanup
demo documentation cleanup
frontend documentation cleanup
repository cleanup
release tag preparation
GitHub release notes
```

The goal is that a reviewer, recruiter, or technical interviewer can open the repository and quickly understand:

```text
what the project does
what currently works
how to run the demo
what is intentionally not included yet
where the project is going next
```

This step is part of the portfolio release.

---

### 2. Real model contract definition

Before connecting a trained model to the platform, the model needs a stable contract.

For the first real GeoAI model, likely a Padena landslide-detection model, the contract should define:

```text
input bands
band order
spatial resolution
tile size
normalisation method
mask classes
output format
threshold policy
model version naming
evaluation metadata
preprocessing rules
postprocessing expectations
```

This is important because the training environment and the platform inference environment must interpret inputs in the same way.

The model should not be treated only as a weights file.

It should be treated as a deployable model package.

---

### 3. Padena landslide model package

A likely first real model integration is a landslide-detection model trained on Sentinel-based imagery for the Padena area in Isfahan, Iran.

The model may be trained outside the platform, for example in:

```text
Kaggle
cloud GPU environment
research computing environment
local experimental workspace
```

Candidate model families may include:

```text
U-Net
DeepLab-based segmentation models
```

The platform itself does not need to train the model at this stage.

The expected output of the research/modeling work should be a structured model package:

```text
trained weights
model architecture reference
preprocessing contract
metrics
threshold policy
sample input
sample output
version metadata
limitations
```

This package can then be connected to the platform through a model adapter and registry entry.

---

### 4. Raster and GeoTIFF input support

The current reproducible demo uses a small JSON-based synthetic payload.

Future GeoAI workflows require real raster support.

This work may include:

```text
GeoTIFF input loading
Cloud Optimized GeoTIFF support
raster metadata extraction
band selection
band order validation
CRS handling
resolution checks
nodata handling
large-scene tiling
```

The goal is to let the platform move from lightweight demo input toward real geospatial data while keeping input loading separate from model implementation.

---

### 5. Preprocessing and postprocessing pipeline

A real satellite-image model requires consistent preprocessing and postprocessing.

Preprocessing may include:

```text
band selection
normalisation
resampling
tiling
mask alignment
cloud or invalid-data handling
conversion to model tensor format
```

Postprocessing may include:

```text
probability thresholding
mask cleanup
polygonization
area calculation
confidence summary
result simplification
export-ready geospatial output
```

These steps should not be hidden inside notebooks.

They should become explicit, testable, and documented parts of the platform workflow.

---

### 6. Result persistence and geospatial output

The platform already has a persistence foundation around:

```text
Dataset
Run
Result
Feedback
```

Future work should expand this into richer geospatial result handling.

This may include:

```text
storing probability masks
storing vectorized result polygons
linking result outputs to model versions
recording input data references
saving summary metrics
capturing user feedback
comparing runs
```

The purpose is to make model outputs traceable and reviewable rather than temporary API responses.

---

### 7. Frontend map interaction

The current frontend is an MVP workspace.

Future frontend work should focus on making the GeoAI workflow more visual and useful.

Possible next steps include:

```text
area-of-interest selection
dataset selection on map
model version selection
execution trigger from the UI
run status display
result preview
probability-mask display
vector overlay display
run comparison
feedback collection
```

The frontend should remain connected to real backend capabilities rather than becoming a static mockup.

---

### 8. Long-running job execution

The current execution model is local and mostly synchronous.

That is acceptable for the current demo and lightweight workflows.

Real raster inference may require longer-running execution.

A later phase may introduce:

```text
background jobs
task queues
worker processes
job status tracking
retry policies
execution logs
GPU-aware execution
resource limits
```

This should be added only when the platform has real workflows that require it.

The goal is not to add infrastructure early for its own sake.

---

### 9. Cloud and deployment improvements

The current project supports a reproducible local Docker workflow.

Future deployment work may include:

```text
production Docker image refinement
environment separation
cloud database configuration
object storage integration
reverse proxy setup
frontend deployment
monitoring dashboards
release automation
backup strategy
```

This belongs after the platform has a stronger real-data and real-model workflow.

For now, local reproducibility is the more important foundation.

---

### 10. Evaluation and model governance

Once real models are connected, the platform should support more explicit evaluation and governance.

This may include:

```text
model evaluation reports
IoU, Dice, precision, recall and F1 tracking
dataset version references
error analysis
model comparison
approved model status
release notes per model version
known limitations
```

The aim is to avoid treating model deployment as a black box.

A model should be explainable in terms of what data it was trained on, how it was evaluated, where it performs well, and where it is still weak.

---

## What is intentionally not prioritized yet

Some capabilities are useful, but they are not immediate priorities.

These include:

```text
multi-tenant authentication
full SaaS billing
distributed cluster orchestration
advanced role-based access control
LLM-based reasoning features
large-scale commercial deployment
complex dashboard analytics
```

They may become relevant later, but adding them too early would distract from the core goal:

```text
a working GeoAI platform connected to real geospatial data and real trained models
```

---

## Suggested next milestones

A realistic next milestone sequence is:

```text
Milestone 1
Public portfolio release of the current platform

Milestone 2
Padena model contract and dataset preparation

Milestone 3
Baseline U-Net or DeepLab model package

Milestone 4
Raster input and preprocessing integration

Milestone 5
First real model adapter inside the platform

Milestone 6
Persisted geospatial result output

Milestone 7
Map-based frontend result visualization

Milestone 8
Improved evaluation, feedback, and model comparison
```

This keeps the project moving from architecture toward real applied GeoAI capability.

---

## Portfolio positioning

For portfolio purposes, the current project demonstrates:

```text
backend architecture
GeoAI platform thinking
FastAPI application design
plugin-based extensibility
PostGIS persistence
model lifecycle preparation
inference orchestration
reproducible demo workflows
frontend-backend integration
documentation and release discipline
```

The future roadmap demonstrates that the project is not just a coding exercise.

It is a foundation for a larger professional direction around GeoAI systems, geospatial data workflows, model integration, and applied environmental-risk analysis.

---

## Current status

The platform foundation is complete enough to be documented, demonstrated, and released as a portfolio project.

The next stage is to connect this foundation to a real GeoAI model and real geospatial data.

The most important next step is not adding random features.

The most important next step is defining and implementing the first real model contract carefully, so that future model development can enter the platform in a controlled and traceable way.