#!/bin/bash

touch celeryconfig.py docker-compose.yaml Dockerfile Dockerfile.nginx Dockerfile.redis nginx.conf redis.conf entrypoint.sh

rm shared/utils/fetch_request_with_error_handlling.py
mv setup.sh series_a_setup.sh

touch shared/config/base_settings.py \
shared/db/connection.py \
shared/utils/fetch_request_with_error_handling.py \
tests/movies/test_tasks.py

python3 -m venv env 
source env/bin/activate

pip install fastapi[standard] flake8 "celery[redis]" coverage gunicorn pymongo psycopg2-binary pytest-cov python-dotenv SQLAlchemy pydantic-settings alembic asyncpg beanie motor
pip freeze > requirements.txt