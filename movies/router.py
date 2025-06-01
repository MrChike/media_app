from fastapi import APIRouter, Query
from typing import Annotated
from .controller import MovieController
from .schema import MovieSchema, MovieResponseSchema


class MovieRouter(APIRouter):
    def __init__(self):
        super().__init__()
        self.controller = MovieController()
        self.add_api_route(path="/omdb/", summary="Fetch Movie from External API", endpoint=self.get_movie, response_model=MovieResponseSchema, methods=["POST"])

    async def get_movie(self, request: Annotated[MovieSchema, Query()]):
        return await self.controller.get_movie(request)


movie_router = MovieRouter()