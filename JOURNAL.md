# Journal entry

## TODO

- create project setup script ✅

## ERRORS/FIXES

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
