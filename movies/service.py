from fastapi import Depends
from sqlalchemy.orm import Session
from .schema import MovieSchema
from shared.config.settings import app_settings
from shared.services.external_apis.omdb_movies import fetch_movie_omdb

class MovieService:
    def __init__(self):
        pass

    async def get_movie_details(self, movie: MovieSchema):
        request_url = f"http://www.omdbapi.com/?apikey={app_settings.omdb_movies_api_key}&type=movie&t={movie.title}&actors={movie.actors}"
        response = await fetch_movie_omdb(request_url)
        return response
