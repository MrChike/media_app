from fastapi import APIRouter, Query
from typing import Annotated
from .controller import MovieController
from .schema import MovieSchema, MovieResponseSchema


class MovieRouter(APIRouter):
    def __init__(self):
        super().__init__()
        self.controller = MovieController()
        self.add_api_route(path="/fetch-omdb-movie/", summary="Fetch Movie from External API", endpoint=self.get_movie, response_model=MovieResponseSchema, methods=["POST"])
        self.add_api_route(path="/create-movie-postgres/", summary="Create Movie in Postgres Database", endpoint=self.create_movie_postgres, methods=["POST"])
        self.add_api_route(path="/create-movie-mongodb/", summary="Create Movie in Mongo Database", endpoint=self.create_movie_mongo, methods=["POST"])
        self.add_api_route(path="/create-movie-external/", summary="Create Movie Using Data Stored in Redis from External API", endpoint=self.create_movie_external, methods=["GET"])
        self.add_api_route(path="/process-heavy-task/", summary="Process Time & Resource Consuming Tasks with Celery", endpoint=self.heavy_task, methods=["GET"])

    async def get_movie(self, request: Annotated[MovieSchema, Query()]):
        return await self.controller.get_movie(request)

    async def create_movie_postgres(self, request: Annotated[MovieSchema, Query()]):
        return await self.controller.create_movie_postgres(request)

    async def create_movie_mongo(self, request: Annotated[MovieSchema, Query()]):
        return await self.controller.create_movie_mongo(request)

    async def create_movie_external(self):
        return await self.controller.create_movie_external()

    def heavy_task(self):
        return self.controller.process_cpu_bound_tasks()


movie_router = MovieRouter()