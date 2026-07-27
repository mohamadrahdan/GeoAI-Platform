# GeoAI Platform Frontend

This folder contains the frontend workspace for GeoAI Platform.

The frontend is built with React, TypeScript, Vite, Leaflet, and React Leaflet. It is currently an MVP workspace, not a finished production interface.

Its purpose is to show how backend execution, plugin discovery, dataset selection, result preview, and map-oriented geospatial interaction can begin to connect in a single user-facing interface.

The main platform logic still lives in the backend. The frontend acts as the early visual layer around that backend workflow.

---

## Current role

At this stage, the frontend helps demonstrate how a user could interact with the platform without calling the API manually.

It provides a foundation for:

- Checking backend connectivity.
- Listing available plugins.
- Loading datasets from the backend.
- Selecting a plugin and dataset.
- Triggering execution requests.
- Displaying loading and error states.
- Previewing returned results.
- Showing a basic map-oriented interface.

The current implementation should be understood as a frontend integration layer, not as a complete GeoAI analysis product yet.

---

## Why the frontend exists

The backend already provides the main platform capabilities: plugin execution, inference, persistence, and API endpoints.

However, geospatial systems are usually easier to understand when results can be explored visually.

The frontend was added to start closing the loop between:

```text
backend execution
→ structured result
→ human inspection
→ map-based interpretation
```

This is especially important for future GeoAI workflows, where users may need to select an area, choose a model, run an analysis, and inspect the result on a map.

---

## Current scope

The current frontend does not yet provide:

- Full production deployment.
- Authentication or user accounts.
- Complete result styling.
- Real raster overlays.
- GeoTIFF or COG visualization.
- Advanced map interaction.
- Long-running job monitoring.
- A polished product-level UI.

Those are future directions.

The current goal is smaller and more practical: provide a working frontend foundation that can communicate with the backend and represent the basic platform workflow.

---

## Tech stack

The frontend uses:

```text
React
TypeScript
Vite
Leaflet
React Leaflet
```

Vite is used for local development and build tooling.

Leaflet and React Leaflet provide the map foundation for future geospatial result visualization.

---

## Backend connection

By default, the frontend expects the backend to be available at:

```text
http://localhost:8000
```

The backend URL can be configured through the frontend environment file.

Create a local environment file from the example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then adjust the backend URL if needed.

The expected variable is defined in:

```text
.env.example
```

---

## Run locally

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The Vite development server will print the local URL in the terminal.

Before using the frontend, make sure the backend stack is running from the repository root:

```bash
docker compose --profile dev up -d --build
```

On Windows PowerShell, the same command can be used:

```powershell
docker compose --profile dev up -d --build
```

---

## Typical local workflow

A typical local development flow is:

```text
1. Start the backend stack from the repository root.
2. Start the frontend development server from the frontend folder.
3. Open the frontend in the browser.
4. Confirm that backend health and plugin data are available.
5. Select a plugin or dataset where supported.
6. Trigger an execution request.
7. Inspect the returned result and map-oriented UI state.
```

This workflow is mainly useful for validating the connection between the browser interface and the backend API.

---

## Build

To create a production build:

```bash
npm run build
```

To preview the build locally:

```bash
npm run preview
```

This does not mean the frontend is already deployed as a production service. It only verifies that the Vite build process works locally.

---

## Relationship to the backend

The frontend does not duplicate backend logic.

It communicates with the backend API and depends on the backend for:

```text
health status
plugin discovery
dataset data
execution requests
result responses
```

The backend remains responsible for core platform behaviour such as plugin execution, inference lifecycle, persistence, and service orchestration.

The frontend is responsible for presenting those capabilities in a more accessible and visual way.

---

## Relationship to future GeoAI workflows

A future landslide-detection workflow could expand this frontend in several directions:

```text
selecting an area of interest
choosing a trained model version
uploading or selecting raster input
triggering inference
showing probability masks
displaying vectorized result areas
comparing runs
reviewing model outputs with user feedback
```

The current frontend does not implement all of that yet.

It provides a starting point so those features can be added gradually without changing the backend architecture every time the user interface grows.

---

## Current status

This frontend is part of the portfolio release of GeoAI Platform.

It is intentionally modest, but it is connected to the larger system direction.

The main value is not that it looks like a finished product today. The value is that the project already has a browser-facing layer that can evolve together with the backend, plugin system, persistence layer, and future model workflows.