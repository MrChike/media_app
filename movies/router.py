from fastapi import APIRouter, Query, Path
from typing import Annotated
from .controller import MovieController
from .schema import MovieSchema


class MovieRouter(APIRouter):
    def __init__(self):
        super().__init__()
        self.controller = MovieController()
        self.add_api_route(
            path="/fetch-omdb-movie/",
            summary="Fetch Movie from External API & Store Data in Redis",
            endpoint=self.get_movie,
            methods=["GET"]
        )
        self.add_api_route(
            path="/create-movie-postgres/",
            summary="Create Movie in Postgres DB",
            endpoint=self.create_movie_postgres,
            methods=["POST"]
        )
        self.add_api_route(
            path="/create-movie-mongodb/",
            summary="Create Movie in MongoDB",
            endpoint=self.create_movie_mongo,
            methods=["POST"]
        )
        self.add_api_route(
            path="/create-movie-external/",
            summary="Create Movie using Title cached from External API.",
            endpoint=self.create_movie_external,
            methods=["POST"]
        )
        self.add_api_route(
            path="/delete-movie/{movie_title}",
            summary="Delete Movie from Redis, Postgres & MongoDB",
            endpoint=self.delete_movie,
            methods=["DELETE"]
        )
        self.add_api_route(
            path="/process-heavy-task/",
            summary="Process Time & Resource Consuming Tasks with Celery",
            endpoint=self.process_heavy_task,
            methods=["POST"]
        )

    async def get_movie(self, request: Annotated[MovieSchema, Query()]):
        return await self.controller.get_movie(request)

    async def create_movie_postgres(
        self, request: Annotated[MovieSchema, Query()]
    ):
        return await self.controller.create_movie_postgres(request)

    async def create_movie_mongo(
        self, request: Annotated[MovieSchema, Query()]
    ):
        return await self.controller.create_movie_mongo(request)

    async def create_movie_external(
        self, request: Annotated[MovieSchema, Query()]
    ):
        return await self.controller.create_movie_external(request)

    async def delete_movie(self, movie_title: Annotated[str, Path()]):
        return await self.controller.delete_movie(movie_title)

    def process_heavy_task(self):
        return self.controller.process_cpu_bound_tasks()


movie_router = MovieRouter()
