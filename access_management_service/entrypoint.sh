#!/bin/sh
set -e

export PYTHONPATH=/app

echo "Running migrations..."
alembic upgrade head

echo "Starting app..."
exec "$@"