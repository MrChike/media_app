#!/bin/bash

touch celeryconfig.py docker-compose.api.yaml docker-compose.db.yaml Dockerfile Dockerfile.nginx nginx.conf entrypoint.sh

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

pip install fastapi[standard] flake8 "celery[redis]" coverage gunicorn pymongo psycopg2-binary pytest-cov python-dotenv SQLAlchemy pydantic-settings alembic asyncpg beanie motor
pip freeze > requirements.txt