import json
import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from movies.service import MovieService, MovieSchema


class TestMovieService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.service = MovieService()
        self.movie_request = MovieSchema(
            title="Inception",
            actors="Leonardo DiCaprio",
            year=2010,
        )

    @patch("movies.service.fetch_movie_omdb", new_callable=AsyncMock)
    @patch("movies.service.RedisClient.set", new_callable=AsyncMock)
    async def test_get_movie_details(
        self, mock_redis_set, mock_fetch_movie_omdb
    ):
        expected_response = {
            'data': {
                'Title': 'Inception',
                'Year': '2010',
                'Actors': 'Leonardo DiCaprio'
            }
        }

        mock_fetch_movie_omdb.return_value = expected_response['data']

        response = await self.service.get_movie_details(self.movie_request)
        movie_title = (
            self.movie_request.title.strip()
            .replace(' ', '_')
            .lower()
        )

        mock_fetch_movie_omdb.assert_awaited_once()
        mock_redis_set.assert_awaited_once_with(
            movie_title,
            json.dumps(expected_response['data'])
        )
        self.assertEqual(response['data'], expected_response['data'])

    @patch("movies.service.movies_db_session")
    async def test_create_movie_postgres(self, mock_movies_db_session):
        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()

        async def mock_db_generator():
            yield mock_db

        mock_movies_db_session.side_effect = mock_db_generator

        result = await self.service.create_movie_postgres(self.movie_request)

        mock_db.add.assert_called()
        mock_db.commit.assert_called()
        self.assertEqual(result["status_code"], 201)
        self.assertEqual(
            result["data"], "Movie Created in Postgres DB Successfully"
        )

    @patch("movies.service.MongoMovie")
    @patch("movies.service.fetch_request_with_error_handling")
    async def test_create_movie_mongo(
        self,
        mock_fetch_request_with_error_handling,
        mock_mongo_movie
    ):
        mock_insert = AsyncMock()
        mock_instance = MagicMock()
        mock_instance.insert = mock_insert
        mock_mongo_movie.return_value = mock_instance

        async def run_func(func, *args, **kwargs):
            await func()
            return {
                "status_code": kwargs.get("status_code", 201),
                "data": kwargs.get("custom_user_success_response", "Success")
            }

        mock_fetch_request_with_error_handling.side_effect = run_func

        result = await self.service.create_movie_mongo(self.movie_request)

        mock_mongo_movie.assert_called_once_with(
            **self.movie_request.model_dump()
        )
        mock_insert.assert_awaited_once()
        self.assertEqual(result["status_code"], 201)
        self.assertEqual(
            result["data"], "Movie Created in Mongo DB Successfully"
        )

    @patch("movies.service.MongoMovie")
    @patch("movies.service.fetch_request_with_error_handling")
    @patch("movies.service.RedisClient.get", new_callable=AsyncMock)
    @patch("movies.service.movies_db_session")
    async def test_create_movie_external_from_cache_success(
        self,
        mock_db_session,
        mock_redis_get,
        mock_fetch_request,
        mock_mongo_movie
    ):
        # Mock Redis response
        fake_movie = {
            "Title": "Inception",
            "Actors": "Leonardo DiCaprio, Joseph Gordon-Levitt",
            "Year": "2010"
        }
        mock_redis_get.return_value = json.dumps(fake_movie)

        # Mock Postgres session
        mock_db = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.add = MagicMock()
        mock_db_session.return_value.__aiter__.return_value = [mock_db]

        # Mock fetch_request_with_error_handling passthrough
        async def passthrough(func, **kwargs):
            return await func()

        mock_fetch_request.side_effect = passthrough

        # Patch MongoMovie instance and insert
        mock_mongo_instance = MagicMock()
        mock_mongo_instance.insert = AsyncMock()
        mock_mongo_movie.return_value = mock_mongo_instance

        # Pass full MovieSchema instance here (FIXED)
        await self.service.create_movie_external_from_cache(self.movie_request)

        mock_mongo_movie.assert_called_once()
        mock_redis_get.assert_awaited_once_with(
            self.movie_request.title.strip().replace(' ', '_').lower()
        )
        mock_mongo_instance.insert.assert_awaited_once()
        mock_db.add.assert_called_once()
        mock_db.commit.assert_awaited_once()

    @patch("movies.service.fetch_request_with_error_handling")
    @patch("movies.service.RedisClient.get", new_callable=AsyncMock)
    async def test_create_movie_external_from_cache_no_data(
        self, mock_redis_get, mock_fetch_request
    ):
        # Simulate Redis having no data
        mock_redis_get.return_value = None

        async def failing_func(func, **kwargs):
            with self.assertRaises(ValueError) as cm:
                await func()
            self.assertEqual(
                str(cm.exception), "No cached movie data found in Redis."
            )

        mock_fetch_request.side_effect = failing_func

        # Pass full MovieSchema instance here (FIXED)
        await self.service.create_movie_external_from_cache(self.movie_request)

    @patch("movies.service.MongoMovie")
    @patch("movies.service.RedisClient.get", new_callable=AsyncMock)
    @patch("movies.service.RedisClient.delete", new_callable=AsyncMock)
    @patch("movies.service.movies_db_session")
    @patch("movies.service.fetch_request_with_error_handling")
    async def test_delete_movie_success(
        self,
        mock_fetch_request,
        mock_db_session,
        mock_redis_delete,
        mock_redis_get,
        mock_mongo_movie,
    ):

        mock_redis_get.return_value = json.dumps({
            "Title": "Inception", "Year": "2010", "Actors": "Leonardo DiCaprio"
        })

        mock_postgres_db = MagicMock()
        mock_result = MagicMock()
        mock_movie_instance = MagicMock()
        mock_result.scalars.return_value.all.return_value = [
            mock_movie_instance
        ]
        mock_postgres_db.execute = AsyncMock(return_value=mock_result)
        mock_postgres_db.delete = AsyncMock()
        mock_postgres_db.commit = AsyncMock()

        async def db_gen():
            yield mock_postgres_db
        mock_db_session.side_effect = db_gen

        mock_mongo_instance = MagicMock()
        mock_mongo_instance.delete = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__.return_value = [mock_mongo_instance]
        mock_mongo_movie.find.return_value = mock_cursor

        # fetch_request_with_error_handling mock
        async def fake_fetch_handler(func, **kwargs):
            await func()
            return {
                "status_code": 200,
                "data": "Movie Deleted Successfully Across all DB"
            }

        mock_fetch_request.side_effect = fake_fetch_handler

        movie_title = (
            self.movie_request.title.strip()
            .replace(' ', '_')
            .lower()
        )
        result = await self.service.delete_movie(movie_title)

        mock_redis_get.assert_awaited_once_with(movie_title)
        mock_redis_delete.assert_awaited_once_with(movie_title)
        mock_postgres_db.execute.assert_awaited()
        mock_postgres_db.delete.assert_awaited_once_with(mock_movie_instance)
        mock_postgres_db.commit.assert_awaited_once()
        mock_mongo_instance.delete.assert_awaited_once()

        self.assertEqual(result["status_code"], 200)
        self.assertEqual(
            result["data"], "Movie Deleted Successfully Across all DB"
        )

    @patch(
        "movies.service.fetch_request_with_error_handling",
        new_callable=AsyncMock
    )
    @patch("movies.service.movies_db_session")
    @patch("movies.service.MongoMovie")
    @patch("movies.service.RedisClient.get", new_callable=AsyncMock)
    async def test_delete_movie_not_found(
        self,
        mock_redis_get,
        mock_mongo_movie,
        mock_db_session,
        mock_fetch_request,
    ):
        movie_title = "Nonexistent Movie"

        # Redis returns nothing
        mock_redis_get.return_value = None

        # PostgreSQL returns no movies
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        async def db_gen():
            yield mock_db
        mock_db_session.side_effect = db_gen

        # MongoDB returns no movies
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__.return_value = []
        mock_mongo_movie.find.return_value = mock_cursor

        # Let the internal fetch_request_with_error_handling call the function
        # directly
        async def fake_handler(func, **kwargs):
            return await func()
        mock_fetch_request.side_effect = fake_handler

        # Instantiate service after patching
        self.service = MovieService()

        # Run and assert exception
        with self.assertRaises(ValueError) as cm:
            await self.service.delete_movie(movie_title)

        self.assertEqual(str(cm.exception), "Movie not found in any DB.")


if __name__ == "__main__":
    unittest.main()
