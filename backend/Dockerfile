# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser


# Install deps (cacheable layer)
COPY backend/requirements.txt /app/requirements.txt
ENV PIP_DEFAULT_TIMEOUT=120 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
#RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --retries 10 --timeout 120 -r /app/requirements.txt


# Copy full repo (so core/ exists)
COPY . /app

USER appuser

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
