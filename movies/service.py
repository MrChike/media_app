import logging
from .schema import MovieSchema
from shared.config.settings import app_settings
from shared.services.external_apis.omdb_movies import fetch_movie_omdb

logger = logging.getLogger(__name__)

class MovieService:
    """
    Constructs the OMDB API URL and calls the fetch function.

    - Catches and logs errors from the fetch call.
    - Returns user-friendly error messages to avoid leaking internal details.
    - Bridges low-level errors with smooth, secure user experience.
    """
    def __init__(self):
        pass

    async def get_movie_details(self, movie: MovieSchema):
        request_url = f"http://www.omdbapi.com/?apikey={app_settings.omdb_movies_api_key}&type=movie&t={movie.title}&actors={movie.actors}"
        try:
            response = await fetch_movie_omdb(request_url)
            return {
                "status_code": 200,
                "data": response
                }
        except Exception as e:
            status_code = 503
            if hasattr(e, "response") and e.response is not None: # type: ignore
                status_code = getattr(e.response, "status_code", status_code) # type: ignore
            logger.error(f"Failed to fetch movie details: {e}")
            return {
                "status_code": status_code,
                "data": "Sorry, we couldn't fetch the movie details right now. Please try again later."
            }