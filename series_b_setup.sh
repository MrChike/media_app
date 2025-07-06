#!/bin/bash

touch celeryconfig.py docker-compose.api.yaml docker-compose.db.yaml Dockerfile Dockerfile.nginx nginx.conf entrypoint.sh

printf "# Note:\n# Containers communicate using Docker Compose service names, ensuring reliable \n# networking without the need to manage specific IP addresses.\n\n# OMDb API Configuration\n# Sign up at https://www.omdbapi.com/apikey.aspx\nOMDB_MOVIES_API_KEY=YOUR_API_KEY_HERE \n\n# PostgreSQL Configuration\nPOSTGRES_USER=root\nPOSTGRES_PASSWORD=root\nPOSTGRES_HOST=localhost\nPOSTGRES_PORT=5432\nPOSTGRES_NAME=root\n\n# MongoDB Configuration\nMONGODB_USER=root\nMONGODB_PASSWORD=root\nMONGODB_HOST=localhost\nMONGODB_PORT=27017\nMONGODB_NAME=root\n\n# Redis Configuration\nREDIS_PASSWORD=root\nREDIS_HOST=localhost\nREDIS_PORT=6379\n" > .example.env

cp .example.env .env
rm shared/utils/fetch_request_with_error_handlling.py
mv setup.sh series_a_setup.sh
mv shared/config/settings.py shared/config/base_settings.py

touch shared/config/settings.py \
shared/db/connection.py \
shared/utils/fetch_request_with_error_handling.py \
tests/movies/test_tasks.py


python3 -m venv env 
source env/bin/activate

pip install fastapi[standard] flake8 "celery[redis]" coverage gunicorn pymongo psycopg2-binary pytest-cov python-dotenv SQLAlchemy pydantic-settings alembic asyncpg beanie motor mkdocs-material
mkdocs new docs && mkdocs build -f docs/mkdocs.yml
pip freeze > requirements.txt