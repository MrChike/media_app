# Journal entry

## TODO

- create project setup script ✅
- make function/method calls async for I/O-bound tasks ✅
- introduce celery for CPU-bound tasks ✅
- introduce Exception Handling ✅
- Explain how code works ✅
- Intoduce Unit testing and coverage report ✅
- Conclude Series A Article ✅
- Write Unit Tests for Service, Task and Controller .py modules ✅
- Set up Docker ✅
- Configure Database for Postgres, Mongo & Redis ✅
- Ensure all configurations are in sync with Series A ✅
- Figure out the best practice for redis to retrieve and create data ✅
- Conclude Unit Tests ✅
- Update README.md ✅
- Update JOURNAL.md ✅
- Write on DB Setup Section in Article ✅
- Write on Crud Operations✅
- Write on Celery Tasks
- Refer to testing setup in part 1
- Write on Project documentation
- Write on Docker Setup
- Conclude Series B Article

## FIXES

```bash
(env) mrchike@practice:~/code/contributions/education/media_app$ uvicorn main:app --reload --port 8000
INFO:     Will watch for changes in these directories: ['/home/mrchike/code/contributions/education/media_app']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [127300] using WatchFiles
Process SpawnProcess-1:
Traceback (most recent call last):
  File "/usr/lib/python3.10/multiprocessing/process.py", line 314, in _bootstrap
    self.run()
  File "/usr/lib/python3.10/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "/home/mrchike/code/contributions/education/media_app/env/lib/python3.10/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
  File "/home/mrchike/code/contributions/education/media_app/env/lib/python3.10/site-packages/uvicorn/server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
  File "/usr/lib/python3.10/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
  File "/home/mrchike/code/contributions/education/media_app/env/lib/python3.10/site-packages/uvicorn/server.py", line 70, in serve
    await self._serve(sockets)
  File "/home/mrchike/code/contributions/education/media_app/env/lib/python3.10/site-packages/uvicorn/server.py", line 77, in _serve
    config.load()
  File "/home/mrchike/code/contributions/education/media_app/env/lib/python3.10/site-packages/uvicorn/config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
  File "/home/mrchike/code/contributions/education/media_app/env/lib/python3.10/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/usr/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 883, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/mrchike/code/contributions/education/media_app/main.py", line 3, in <module>
    from movies.router import movie_router
  File "/home/mrchike/code/contributions/education/media_app/movies/router.py", line 3, in <module>
    from .controller import MovieController
  File "/home/mrchike/code/contributions/education/media_app/movies/controller.py", line 4, in <module>
    from .service import MovieService
  File "/home/mrchike/code/contributions/education/media_app/movies/service.py", line 3, in <module>
    from .model import Movie  # your ORM model
  File "/home/mrchike/code/contributions/education/media_app/movies/model.py", line 2, in <module>
    from shared.db.connection import Base
  File "/home/mrchike/code/contributions/education/media_app/shared/db/connection.py", line 3, in <module>
    from shared.config.settings import app_settings
  File "/home/mrchike/code/contributions/education/media_app/shared/config/settings.py", line 28, in <module>
    app_settings = AppSettings() # type: ignore
  File "/home/mrchike/code/contributions/education/media_app/env/lib/python3.10/site-packages/pydantic_settings/main.py", line 176, in __init__
    super().__init__(
  File "/home/mrchike/code/contributions/education/media_app/env/lib/python3.10/site-packages/pydantic/main.py", line 253, in __init__
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
pydantic_core._pydantic_core.ValidationError: 1 validation error for AppSettings
spotify_music_api_key
  Field required [type=missing, input_value={'omdb_movies_api_key': '...', 'redis_port': '6379'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/missing

solution: Spotify API Key was not available in .env was causing issues so had to remove it from media_app/shared/config/settings.py AppSettings class
```

```bash
(env) mrchike@practice:~/code/contributions/education/media_app$ pytest
==================================================== test session starts ====================================================
platform linux -- Python 3.10.12, pytest-8.3.5, pluggy-1.6.0
rootdir: /home/mrchike/code/contributions/education/media_app
configfile: pytest.ini
testpaths: tests/
plugins: anyio-4.9.0, cov-6.1.1
collected 0 items / 1 error                                                                                                 
/home/mrchike/code/contributions/education/media_app/env/lib/python3.10/site-packages/coverage/control.py:915: CoverageWarning: No data was collected. (no-data-collected)
  self._warn("No data was collected.", slug="no-data-collected")

========================================================== ERRORS ===========================================================
_____________________________________ ERROR collecting tests/movies/test_controller.py ______________________________________
ImportError while importing test module '/home/mrchike/code/contributions/education/media_app/tests/movies/test_controller.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/movies/test_controller.py:4: in <module>
    from media_app.movies.controller import MovieController
E   ModuleNotFoundError: No module named 'media_app'
====================================================== tests coverage =======================================================
_____________________________________ coverage: platform linux, python 3.10.12-final-0 ______________________________________

Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
movies/controller.py      10     10     0%   1-13
movies/service.py         19     19     0%   1-32
movies/tasks.py            0      0   100%
----------------------------------------------------
TOTAL                     29     29     0%
================================================== short test summary info ==================================================
ERROR tests/movies/test_controller.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
===================================================== 1 error in 2.68s ======================================================


Step 1/6 : FROM python:3.12-alpine
 ---> 2d6c23e3d401
Step 2/6 : WORKDIR /code
 ---> Running in 1d042334119f
 ---> Removed intermediate container 1d042334119f
 ---> a77be17e6d54
Step 3/6 : COPY ./requirements.txt /
 ---> 4cda42078333
Step 4/6 : RUN pip install --root-user-action=ignore --upgrade pip
 ---> Running in 047c2aba37ba
Requirement already satisfied: pip in /usr/local/lib/python3.12/site-packages (25.0.1)
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x71a210e79b80>: Failed to establish a new connection: [Errno -3] Try again')': /simple/pip/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x71a20fbdbfb0>: Failed to establish a new connection: [Errno -3] Try again')': /simple/pip/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x71a20fc5c080>: Failed to establish a new connection: [Errno -3] Try again')': /simple/pip/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x71a20fc5c2c0>: Failed to establish a new connection: [Errno -3] Try again')': /simple/pip/
WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x71a20fc5c500>: Failed to establish a new connection: [Errno -3] Try again')': /simple/pip/
 ---> Removed intermediate container 047c2aba37ba
 ---> 2a195dad4461
Step 5/6 : RUN pip install --root-user-action=ignore -r /requirements.txt
 ---> Running in 14a44d77e9f2
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7361446ef5c0>: Failed to establish a new connection: [Errno -3] Try again')': /simple/alembic/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7361463430e0>: Failed to establish a new connection: [Errno -3] Try again')': /simple/alembic/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7361446efb30>: Failed to establish a new connection: [Errno -3] Try again')': /simple/alembic/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7361446efd40>: Failed to establish a new connection: [Errno -3] Try again')': /simple/alembic/
WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7361446eff20>: Failed to establish a new connection: [Errno -3] Try again')': /simple/alembic/
ERROR: Could not find a version that satisfies the requirement alembic==1.16.2 (from versions: none)
ERROR: No matching distribution found for alembic==1.16.2
The command '/bin/sh -c pip install --root-user-action=ignore -r /requirements.txt' returned a non-zero code: 1

Solution: sudo systemctl restart docker
```

<!-- Important NB: Always open project root in Favourite IDE to prevent import modules import issues -->

```bash
$ docker-compose down --remove-orphans && docker-compose build && docker-compose up --force-recreate
$ alembic revision --autogenerate -m "Migration Message"
$ alembic upgrade head
$ uvicorn main:app --reload --port 8000
$ sudo systemctl restart docker.service
$ sudo shutdown -r now

# NB: If container isn't displaying content on browser
$ docker image ls 

(env) mrchike@mrchike-vm:~/code/media_app$ docker image ls
REPOSITORY           TAG                   IMAGE ID       CREATED         SIZE
<none>               <none>                bcf8acc6fac1   2 minutes ago   48.7MB
media_app_redis      latest                8508c6032e82   2 minutes ago   128MB

$ docker rmi bcf8acc6fac1 8508c6032e82 .....

$ docker-compose -f docker-compose.db.yaml -f docker-compose.api.yaml down --remove-orphans &&  docker-compose -f docker-compose.db.yaml -f docker-compose.api.yaml up --build --force-recreate

$ docker rmi -f media_app_nginx:latest media_app_api:latest media_app_celery:latest media_app_redis:latest

$ docker-compose -f docker-compose.db.yaml down --remove-orphans && docker-compose -f docker-compose.db.yaml up
```

# How to check code diff with VSCode
```bash
$ git config --global diff.tool vscode
$ git config --global difftool.vscode.cmd 'code --wait --diff "$LOCAL" "$REMOTE"'

$ git config --global difftool.prompt false
$ git log --oneline

(env) mrchike@mrchike-vm:~/code/media_app$ git log --oneline
6dba06b (HEAD -> series_b) partial conclusion
518aeb3 (origin/series_b) Add delete movie endpoint

(env) mrchike@mrchike-vm:~/code/media_app$ git diff --name-only 518aeb3 6dba06b
JOURNAL.md
entrypoint.sh
movies/service.py
shared/services/external_apis/omdb_movies.py
shared/utils/fetch_request_with_error_handling.py
tests/movies/test_service.py

$ git difftool 518aeb3 6dba06b movies/service.py

```
## Remove .pyc files from project
`find . -type d -name "__pycache__" -exec rm -r {} + -o -name "*.pyc" -exec rm -f {} +`
