#!/bin/bash

echo "Waiting for elastic to get up and running..."
while ! nc -z elastic ${ELASTIC_PORT}; do
  sleep 1
done
echo "elastic started"

gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
