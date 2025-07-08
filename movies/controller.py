from fastapi import Response
from fastapi.responses import JSONResponse
from .schema import MovieSchema
from .service import MovieService


class MovieController:
    def __init__(self):
        self.service = MovieService()

    # movie request is validated & serialized by MovieSchema
    async def get_movie(
        self, request: MovieSchema
    ) -> Response:
        response = await self.service.get_movie_details(request)
        return JSONResponse(
            content={"data": response["data"]},
            status_code=response["status_code"]
        )

    async def create_movie_postgres(self, request: MovieSchema) -> Response:
        response = await self.service.create_movie_postgres(request)
        return JSONResponse(
            content={"data": response["data"]},
            status_code=response["status_code"]
        )

    async def create_movie_mongo(self, request: MovieSchema) -> Response:
        response = await self.service.create_movie_mongo(request)
        return JSONResponse(
            content={"data": response["data"]},
            status_code=response["status_code"]
        )

    async def create_movie_external(self, request: MovieSchema) -> Response:
        response = await self.service.create_movie_external_from_cache(request)
        return JSONResponse(
            content={"data": response["data"]},
            status_code=response["status_code"]
        )

    async def delete_movie(self, movie_title: str) -> Response:
        response = await self.service.delete_movie(movie_title)
        return JSONResponse(
            content={"data": response["data"]},
            status_code=response["status_code"]
        )
