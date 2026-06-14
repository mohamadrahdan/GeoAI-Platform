#!/bin/bash

# Stop if any errors occur
set -e

echo "🚀 Starting GeoAI-Platform Deployment Process..."

# 1. Pull latest changes from the main branch
echo "📥 Pulling latest code from repository..."
git pull origin main

# 2. Rebuild the Docker images to catch any new dependencies
echo "📦 Building Docker images..."
docker compose -f docker-compose.yml build

# 3. Start the containers (detached mode) and remove orphan containers
echo "🔄 Starting containers..."
docker compose -f docker-compose.yml up -d --remove-orphans

# 4. Prune unused docker images to save VPS disk space
echo "🧹 Cleaning up old unused images..."
docker image prune -f

echo "✅ Deployment Successful! GeoAI-Platform is up and running."