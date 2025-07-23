#!/bin/bash

# ==============================================================================
# Script: series_b_setup.sh
# Purpose: Set up core infrastructure, environment configs, and project scaffolding
# ==============================================================================

# ------------------------------------------------------------------------------
# Create core infrastructure and configuration files
# ------------------------------------------------------------------------------
touch celeryconfig.py docker-compose.api.yaml docker-compose.db.yaml Dockerfile Dockerfile.nginx nginx.conf entrypoint.sh

# ------------------------------------------------------------------------------
# Generate example environment configuration
# ------------------------------------------------------------------------------
cat <<EOF > .example.env
# Note:
# Containers communicate using Docker Compose service names, ensuring reliable 
# networking without the need to manage specific IP addresses.

# OMDb API Configuration
# Sign up at https://www.omdbapi.com/apikey.aspx
OMDB_MOVIES_API_KEY=YOUR_API_KEY_HERE

# PostgreSQL Configuration
POSTGRES_USER=root
POSTGRES_PASSWORD=root
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_NAME=root

# MongoDB Configuration
MONGODB_USER=root
MONGODB_PASSWORD=root
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_NAME=root

# Redis Configuration
REDIS_PASSWORD=root
REDIS_HOST=localhost
REDIS_PORT=6379
EOF

# ------------------------------------------------------------------------------
# Copy example environment to actual environment
# ------------------------------------------------------------------------------
cp .example.env .env

# ------------------------------------------------------------------------------
# Update import path in movie service
# ------------------------------------------------------------------------------
FILE="./movies/service.py"
sed -i 's|from shared.config.settings import app_settings|from shared.config.base_settings import app_settings|' "$FILE"

# ------------------------------------------------------------------------------
# Cleanup and refactor configuration structure
# ------------------------------------------------------------------------------
rm shared/utils/fetch_request_with_error_handlling.py
mv setup.sh series_a_setup.sh
mv shared/config/settings.py shared/config/base_settings.py

# ------------------------------------------------------------------------------
# Define base settings with Pydantic
# ------------------------------------------------------------------------------
cat <<EOF > shared/config/base_settings.py
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings(BaseSettings):
    omdb_movies_api_key: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_name: str
    mongodb_user: str
    mongodb_password: str
    mongodb_host: str
    mongodb_port: int
    mongodb_name: str
    redis_password: str
    redis_host: str
    redis_port: str


app_settings = AppSettings()  # type: ignore

EOF

# ------------------------------------------------------------------------------
# Create missing project files
# ------------------------------------------------------------------------------
touch shared/config/settings.py \
      shared/db/connection.py \
      shared/utils/fetch_request_with_error_handling.py \
      tests/movies/test_tasks.py

# ------------------------------------------------------------------------------
# Create and reorganize test folder structure
# ------------------------------------------------------------------------------
mkdir -p tests/unit \
         tests/integration/base \
         tests/integration/movies \
         tests/e2e \
         tests/system

mv tests/base tests/unit
mv tests/movies tests/unit

# Add __init__.py files for test modules
find tests -type d -exec touch {}/__init__.py \;

# ------------------------------------------------------------------------------
# Set up Python virtual environment and install dependencies
# ------------------------------------------------------------------------------
python3 -m venv env 
source env/bin/activate

pip install fastapi[standard] flake8 "celery[redis]" coverage gunicorn pymongo psycopg2-binary pytest-cov python-dotenv SQLAlchemy pydantic-settings alembic asyncpg beanie motor mkdocs-material
pip freeze > requirements.txt

# ------------------------------------------------------------------------------
# Initialize MkDocs documentation structure
# ------------------------------------------------------------------------------
mkdocs new docs 
mkdir -p docs/docs/assets/images

touch docs/docs/architecture.md \
      docs/docs/changelog.md \
      docs/docs/contact.md \
      docs/docs/contributing.md \
      docs/docs/features.md

# ------------------------------------------------------------------------------
# Project Documentation Configuration
# ------------------------------------------------------------------------------
cat <<EOF > docs/mkdocs.yml
site_name: Project Documentation
repo_name: MrChike/media_app # Replace with your repository name

nav:
  - Home: index.md
  - Features: features.md
  - Architecture: architecture.md
  - Contributing: contributing.md
  - Changelog: changelog.md
  - Contact: contact.md

theme:
  name: material
  favicon: https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/materialformkdocs.svg
  features:
    - toc.integrate
    - navigation.tabs
    - navigation.footer

extra_css:
  - assets/stylesheets/extra.css

extra_javascript:
  - assets/javascripts/extra.js

EOF

curl -o docs/docs/assets/images/logo.png https://e7.pngegg.com/pngimages/574/377/png-clipart-logo-retro-bar-design-text-trademark.png
mkdocs build -f docs/mkdocs.yml
