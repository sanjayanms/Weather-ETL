#!/bin/bash
echo "AWS Login..."
aws login

echo "Docker Login..."
docker login

echo "Stopping containers..."
docker compose down

echo "Removing stopped containers..."
docker container prune -f

echo "Removing Airflow image..."
docker images -q weather-airflow | grep -q . && docker rmi -f weather-airflow:latest


echo "Removing unused volumes..."
docker volume prune -f

echo "Removing unused networks..."
docker network prune -f

echo "Initializing Airflow..."
DOCKER_BUILDKIT=0 docker build -t weather-airflow:latest .

echo "Starting Airflow services..."
docker compose up 

echo "Done!"
