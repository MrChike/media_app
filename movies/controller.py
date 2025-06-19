from fastapi import Response
from fastapi.responses import JSONResponse
from .schema import MovieSchema
from .service import MovieService


class MovieController:
    def __init__(self):
        self.service = MovieService()

    async def get_movie(self, request: MovieSchema) -> Response:  # movie request is validated & serialized by MovieSchema
        response = await self.service.get_movie_details(request)
        return JSONResponse(content={"data": response["data"]}, status_code=response["status_code"])

    async def create_movie_postgres(self, request: MovieSchema) -> Response:
        response = await self.service.create_movie_postgres(request)
        return JSONResponse(content={"data": response["data"]}, status_code=response["status_code"])

    async def create_movie_mongo(self, request: MovieSchema) -> Response:
        response = await self.service.create_movie_mongo(request)
        return JSONResponse(content={"data": response["data"]}, status_code=response["status_code"])

    async def create_movie_external(self) -> Response:
        response = await self.service.create_movie_external_from_cache()
        return JSONResponse(content={"data": response["data"]}, status_code=response["status_code"])

    def process_cpu_bound_tasks(self) -> Response:
        self.service.trigger_cpu_bound_task()
        return JSONResponse(content={"data": "Background Task is processing..."}, status_code=200)
