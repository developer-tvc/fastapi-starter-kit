#!/bin/bash

echo "Waiting for PostgreSQL..."

while ! pg_isready -h host.docker.internal -p 5432 -U postgres
do
  sleep 2
done

echo "Database started"

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI..."

uvicorn app.main:app --host 0.0.0.0 --port 8000