#!/bin/bash

echo "---------- Creating container for running tests ------------"
CONTAINER_ID=$(docker run -d market-spread-api)
echo "---------- Running tests ------------"
docker exec "$CONTAINER_ID" poetry run python manage.py test
echo "---------- Stopping container ------------"
docker stop "$CONTAINER_ID"