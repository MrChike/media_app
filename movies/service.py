import json
import logging
from sqlalchemy import select
from shared.db.connection import RedisClient
from shared.config.base_settings import app_settings
from shared.utils.fetch_request_with_error_handling import (
    fetch_request_with_error_handling,
)
from shared.services.external_apis.omdb_movies import fetch_movie_omdb
from .dependencies import movies_db_session
from .model import PostgresMovie, MongoMovie
from .schema import MovieSchema
from .tasks import process_heavy_task


logger = logging.getLogger(__name__)


class MovieService:
    """
    Service for interacting with the OMDB API and local movie database.

    - Fetches movie details from OMDB.
    - Adds movies to the local database.
    - Handles exceptions gracefully and logs errors.
    """
    def __init__(self):
        self.session = movies_db_session()

    async def get_movie_details(self, movie: MovieSchema):
        async def _get_movie_details():
            api_key = app_settings.omdb_movies_api_key
            request_url = (
                f"http://www.omdbapi.com/?apikey={api_key}"
                f"&type=movie&t={movie.title}"
            )

            if movie.year:
                request_url += f"&y={movie.year}"

            response_data = await fetch_movie_omdb(request_url)

            if 'Title' in response_data:
                movie_title = (
                    response_data['Title']
                    .strip()
                    .replace(' ', '_')
                    .lower()
                )
                await RedisClient.set(movie_title, json.dumps(response_data))

            return response_data

        return await fetch_request_with_error_handling(
            _get_movie_details,
            custom_user_error_response=(
                "We couldn't fetch the movie details from OMDB API. "
                "Please try again later."
            )
        )

    async def create_movie_postgres(self, request: MovieSchema):
        async def _create_movie_postgres():
            async for db in movies_db_session():
                # NB: Postgres Movie Model has None as default
                # so if actors or years is left blank it's Null
                postgres_movie = PostgresMovie(
                    title=request.title,
                    actors=request.actors,
                    year=request.year or 1900
                )

                db.add(postgres_movie)
                await db.commit()
        return await fetch_request_with_error_handling(
            _create_movie_postgres,
            status_code=201,
            custom_user_success_response=(
                "Movie Created in Postgres DB Successfully"
            ),
            custom_user_error_response=(
                "Unable to create movie record in postgres DB right now. "
                "Please try again later."
            )
        )

    async def create_movie_mongo(self, movie_data: MovieSchema):
        async def _create_movie_mongo():
            movie = MovieSchema(
                title=movie_data.title,
                actors=movie_data.actors or " ",
                year=movie_data.year or 1900
            )
            mongo_movie = MongoMovie(**movie.model_dump())
            await mongo_movie.insert()

        return await fetch_request_with_error_handling(
            _create_movie_mongo,
            status_code=201,
            custom_user_success_response=(
                "Movie Created in Mongo DB Successfully"
            ),
            custom_user_error_response=(
                "Unable to create movie record in mongo DB right now. "
                "Please try again later."
            )
        )

    async def create_movie_external_from_cache(self, request: MovieSchema):
        async def _create_movie_external_from_cache():
            movie_title = request.title.strip().replace(' ', '_').lower()
            data = await RedisClient.get(movie_title)

            if not data:
                raise ValueError("No cached movie data found in Redis.")

            movie = json.loads(data)

            title = movie["Title"].strip().replace(' ', '_').lower()
            actors = movie["Actors"]
            year = int(movie["Year"])

            # Process & Save Data in Postgres DB
            async for db in movies_db_session():
                postgres_movie = PostgresMovie(
                    title=title,
                    actors=actors,
                    year=year
                )
                db.add(postgres_movie)
                await db.commit()

            # Process & Save Data in MongoDB
            mongo_movie_data = MovieSchema(
                title=title,
                actors=actors,
                year=year
            )

            mongo_movie = MongoMovie(**mongo_movie_data.model_dump())
            await mongo_movie.insert()

        return await fetch_request_with_error_handling(
            _create_movie_external_from_cache,
            custom_user_success_response=(
                "Movie Created Successfully in both Postgres & MongoDB "
                "from Redis DB Cache"
            ),
            custom_user_error_response="Movie Record not Found!"
        )

    async def delete_movie(self, movie_title: str):
        async def _delete_movie_from_all_db():
            movie = movie_title.strip().replace(' ', '_').lower()
            movie_found = False  # Track if any DB has the movie

            # Redis
            redis_movie = await RedisClient.get(movie)
            if redis_movie:
                movie_found = True
                await RedisClient.delete(movie)
            else:
                logger.error("============== ERROR =================")
                logger.error("No cached movie found in Redis.")
                logger.error("======================================")

            # PostgreSQL
            async for db in movies_db_session():
                result = await db.execute(
                    select(PostgresMovie).where(PostgresMovie.title == movie)
                )
                postgres_movies = result.scalars().all()

                if postgres_movies:
                    movie_found = True
                    for postgres_movie in postgres_movies:
                        await db.delete(postgres_movie)
                    await db.commit()

            # MongoDB
            mongo_movies_cursor = MongoMovie.find(MongoMovie.title == movie)
            found_in_mongo = False
            async for mongo_movie in mongo_movies_cursor:
                found_in_mongo = True
                await mongo_movie.delete()

            if found_in_mongo:
                movie_found = True

            # If not found in any DB, raise to trigger custom error response
            if not movie_found:
                raise ValueError("Movie not found in any DB.")

        return await fetch_request_with_error_handling(
            _delete_movie_from_all_db,
            custom_user_success_response=(
                "Movie Deleted Successfully Across all DB"
            ),
            custom_user_error_response="Movie not found in DB"
        )

    def trigger_cpu_bound_task(self):
        process_heavy_task.delay()  # type: ignore
