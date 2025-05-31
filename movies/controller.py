from fastapi import Response, status
from fastapi.responses import JSONResponse
from .schema import MovieSchema
from .service import MovieService

class MovieController:
    def __init__(self):
        self.service = MovieService()

    async def get_movie(self, request: MovieSchema) -> Response: # movie request is already validated by MovieSchema
        response = await self.service.get_movie_details(request)

        return JSONResponse(content={"data": response}, status_code=status.HTTP_200_OK)
