#!/bin/bash
set -e

# Fix line endings
sed -i 's/\r$//' setup_server.sh
sed -i 's/\r$//' docker-compose.yml

# Ensure nginx config exists
mkdir -p ./nginx_conf
if [ ! -f ./nginx_conf/default.conf ]; then
    echo "First run: Setting up default Nginx config..."
    cp ./frontend/nginx.conf ./nginx_conf/default.conf
fi

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
