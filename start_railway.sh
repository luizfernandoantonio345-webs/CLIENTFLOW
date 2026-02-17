#!/bin/bash
# Railway Startup Script - Run migrations then start server

set -e  # Exit on error

echo "🔄 Running Alembic migrations..."
alembic upgrade head

echo "🚀 Starting Gunicorn server..."
exec gunicorn backend.main:app \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
