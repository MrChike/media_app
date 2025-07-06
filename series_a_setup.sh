python3 -m venv env 
source env/bin/activate

touch .example.env .coveragerc .gitignore main.py pytest.ini requirements.txt JOURNAL.md README.md

printf "# OMDb API Configuration\n# Sign up at https://www.omdbapi.com/apikey.aspx\n\nOMDB_MOVIES_API_KEY=YOUR_API_KEY_HERE \n\n# DB config\nDB_USER=root\nDB_PASSWORD=root\nDB_HOST=localhost\nDB_PORT=5432\nDB_NAME=root\n\n# Redis config\nREDIS_PASSWORD=root\nREDIS_HOST=localhost\nREDIS_PORT=6379" > .example.env

cp .example.env .env

mkdir -p static templates docs \
shared/config \
shared/dependencies \
shared/middleware \
shared/services/external_apis \
shared/services/internal_operations \
shared/utils \
scripts \
tests/base \
tests/movies \
base && \

touch shared/__init__.py \
shared/config/__init__.py \
shared/config/settings.py \
shared/dependencies/__init__.py \
shared/middleware/__init__.py \
shared/services/__init__.py \
shared/utils/__init__.py \
shared/services/external_apis/__init__.py \
shared/services/external_apis/omdb_movies.py \
shared/services/internal_operations/__init__.py \
scripts/__init__.py \
scripts/sanity_check.py \
tests/__init__.py \
tests/base/__init__.py \
tests/movies/__init__.py \
tests/movies/test_controller.py \
tests/movies/test_service.py \
base/__init__.py \
base/router.py \
base/controller.py \
base/service.py \
base/model.py \
base/schema.py \
base/dependencies.py \
base/tasks.py

printf "%s\n" "*.log" "*.pot" "*.pyc" "__pycache__" "db.sqlite3" "media" "htmlcov/" ".tox/" ".coverage" ".coverage.*" "**/.coverage" "**/.coverage.*" ".cache" ".pytest_cache/" "nosetests.xml" "coverage.xml" "*.cover" ".hypothesis/" "site" ".vscode/*" ".history" "**/__
pycache__/" ".env" "env/" > .gitignore

pip install fastapi[standard] flake8 "celery[redis]" coverage gunicorn pymongo psycopg2-binary pytest-cov python-dotenv SQLAlchemy pydantic-settings
pip freeze > requirements.txt
