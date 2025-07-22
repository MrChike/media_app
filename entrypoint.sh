#!/bin/bash
set -e

echo "Running as user: $(whoami)"

echo ""
echo "🔧 Building the documentation site with MkDocs..."
echo ""
mkdocs build -f docs/mkdocs.yml

echo ""
echo "💡 Reminder:"
echo "   If you've updated or changed models, don't forget to run:"
echo "   👉 alembic revision --autogenerate -m 'YOUR MIGRATION MESSAGE'"
echo ""

echo ""
echo "🚀 Running Alembic migrations..."
echo ""
alembic upgrade head

echo ""
echo "🧪 Running tests..."
echo ""
pytest

echo ""
echo "🚀 Starting FastAPI app with Gunicorn..."
echo ""
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info