#!/bin/sh
set -e

echo "Running Alembic migrations..."
until alembic upgrade head; do
  echo "Migration failed (DB might not be ready). Retrying in 3s..."
  sleep 3
done

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
