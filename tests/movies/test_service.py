import json
import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from movies.service import MovieService, MovieSchema


class TestMovieService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.service = MovieService()
        self.movie_request = MovieSchema(title="Inception", actors="Leonardo DiCaprio", year=2010)

    @patch("movies.service.fetch_request_with_error_handling", new_callable=AsyncMock)
    @patch("movies.service.RedisClient.set", new_callable=AsyncMock)
    async def test_get_movie_details(self, mock_redis_set, mock_fetch_request_with_error_handling):
        expected_response_data = {
            'status_code': 200, 
            'data': {'Title': 'Inception', 'Year': '2010', 'Actors': 'Leonardo DiCaprio'}
        }

        mock_fetch_request_with_error_handling.return_value = expected_response_data

        response = await self.service.get_movie_details(self.movie_request)

        mock_fetch_request_with_error_handling.assert_awaited_once()
        mock_redis_set.assert_awaited_once_with("Movie Data", json.dumps(expected_response_data["data"]))
        self.assertEqual(response, expected_response_data)

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
        self.assertEqual(result["data"], "Movie Created in Postgres DB Successfully")

    @patch("movies.service.MovieMongo")
    @patch("movies.service.fetch_request_with_error_handling")
    async def test_create_movie_mongo(self, mock_fetch_request_with_error_handling, mock_movie_mongo):
        mock_insert = AsyncMock()
        mock_instance = MagicMock()
        mock_instance.insert = mock_insert
        mock_movie_mongo.return_value = mock_instance

        async def run_func(func, *args, **kwargs):
            await func()
            return {
                "status_code": kwargs.get("status_code", 201),
                "data": kwargs.get("custom_user_success_response", "Success")
            }

        mock_fetch_request_with_error_handling.side_effect = run_func

        result = await self.service.create_movie_mongo(self.movie_request)

        mock_movie_mongo.assert_called_once_with(**self.movie_request.model_dump())
        mock_insert.assert_awaited_once()
        self.assertEqual(result["status_code"], 201)
        self.assertEqual(result["data"], "Movie Created in Mongo DB Successfully")

    @patch("movies.service.MovieMongo")  # Patch the class only
    @patch("movies.service.fetch_request_with_error_handling")
    @patch("movies.service.RedisClient.get", new_callable=AsyncMock)
    @patch("movies.service.movies_db_session")
    async def test_create_movie_external_from_cache_success(
        self, mock_db_session, mock_redis_get, mock_fetch_request, mock_movie_mongo
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

        # Patch MovieMongo instance and insert
        mock_mongo_instance = MagicMock()
        mock_mongo_instance.insert = AsyncMock()
        mock_movie_mongo.return_value = mock_mongo_instance

        await self.service.create_movie_external_from_cache()

        mock_movie_mongo.assert_called_once()
        mock_redis_get.assert_awaited_once_with("Movie Data")
        mock_mongo_instance.insert.assert_awaited_once()
        mock_db.add.assert_called_once()
        mock_db.commit.assert_awaited_once()

    @patch("movies.service.fetch_request_with_error_handling")
    @patch("movies.service.RedisClient.get", new_callable=AsyncMock)
    async def test_create_movie_external_from_cache_no_data(self, mock_redis_get, mock_fetch_request):
        # Simulate Redis having no data
        mock_redis_get.return_value = None

        async def failing_func(func, **kwargs):
            with self.assertRaises(ValueError) as cm:
                await func()
            self.assertEqual(str(cm.exception), "No cached movie data found in Redis.")

        mock_fetch_request.side_effect = failing_func

        await self.service.create_movie_external_from_cache()
        
    @patch("movies.service.process_heavy_task")
    def test_trigger_cpu_bound_task_calls_delay(self, mock_task):
        self.service.trigger_cpu_bound_task()
        mock_task.delay.assert_called_once()


if __name__ == "__main__":
    unittest.main()
