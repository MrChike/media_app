from beanie import init_beanie
from movies.model import MongoMovie


async def init_mongo():
    from shared.db.connection import MongoDB
    await init_beanie(
        database=MongoDB,
        # NB: All Mongo DB's models created should be registered in this list
        document_models=[
            MongoMovie
        ]
    )
