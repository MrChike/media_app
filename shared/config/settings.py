from beanie import init_beanie
from celery import Celery
from movies.model import MongoMovie


redis_broker = Celery('tasks')
redis_broker.config_from_object('celeryconfig')

# NB Makes tasks visible to celery upon app loading.
# The import must come after
# redis_broker.config_from_object('celeryconfig')

# TODO: Find a neat way to register celery tasks
import movies.tasks


async def init_mongo():
    from shared.db.connection import MongoDB
    await init_beanie(
        database=MongoDB,
        # NB: All Mongo DB's models created should be registered in this list
        document_models=[
            MongoMovie
        ]
    )
