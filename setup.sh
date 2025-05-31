python3 -m venv env 
source env/bin/activate

touch .example.env .coveragerc .gitignore main.py pytest.ini requirements.txt JOURNAL.md README.md

mkdir -p static templates docs \
shared/config \
shared/dependencies \
shared/middleware \
shared/services/external_apis \
shared/services/internal_operations \
shared/utils \
scripts \
tests/base \
base && \

touch shared/__init__.py \
shared/config/__init__.py \
shared/config/settings.py \
shared/dependencies/__init__.py \
shared/middleware/__init__.py \
shared/services/__init__.py \
shared/utils/__init__.py \
shared/services/external_apis/__init__.py \
shared/services/internal_operations/__init__.py \
scripts/__init__.py \
scripts/sanity_check.py \
tests/__init__.py \
tests/base/__init__.py \
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

pip install fastapi[standard] flake8 "celery[redis]" coverage gunicorn pymongo psycopg2-binary pytest-cov python-dotenv SQLAlchemy
pip freeze > requirements.txt
