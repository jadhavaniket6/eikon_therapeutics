#!/bin/bash

# Build Docker image
docker build -t my-flask-app .

docker run -p 6000:5000 my-flask-app &

sleep 3

container_name=$(docker ps --format "{{.Names}}")

# Perform curl requests
docker exec $container_name curl -X GET http://localhost:5000/
docker exec $container_name curl -X GET http://localhost:5000/show_data

#Below cmd will only execute if a proper database is provided
# curl -X POST http://localhost:5000/trigger_etl

#Stop and remove the container
docker stop $container_name

docker rm $container_name

echo "Docker container stopped and removed. Process completed."
