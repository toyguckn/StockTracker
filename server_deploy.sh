#!/bin/bash
set -e

# Fix line endings
sed -i 's/\r$//' setup_server.sh
sed -i 's/\r$//' docker-compose.yml

# Setup
chmod +x setup_server.sh
./setup_server.sh

# Stop containers
docker compose down --remove-orphans || true

# Build SEQUENTIALLY to save memory
echo "Building Backend..."
docker compose build backend

echo "Building Scraper..."
docker compose build scraper

echo "Building Frontend..."
docker compose build frontend

# Start
echo "Starting Services..."
docker compose up -d
