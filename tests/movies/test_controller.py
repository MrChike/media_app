import json
import unittest
from unittest.mock import AsyncMock, MagicMock
from fastapi.responses import JSONResponse
from movies.controller import MovieController
from movies.schema import MovieSchema


class TestMovieController(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.controller = MovieController()
        self.controller.service = MagicMock()
        self.mock_request = MovieSchema(title="Inception")

    async def test_get_movie(self):
        expected_response_data = {
            "title": "Inception",
            "actors": "Leonardo DiCaprio",
            "year": 2010
        }

        self.controller.service.get_movie_details = AsyncMock(
            return_value={"data": expected_response_data, "status_code": 200}
        )

        response = await self.controller.get_movie(self.mock_request)

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body), {
            "data": {
                "title": "Inception",
                "actors": "Leonardo DiCaprio",
                "year": 2010
            }
        })

    async def test_create_movie_postgres(self):
        expected_response_data = {
            'data': 'Movie Created in Postgres DB Successfully'
        }

        self.controller.service.create_movie_postgres = AsyncMock(
            return_value={
                "data": expected_response_data['data'],
                "status_code": 201
            }
        )

        response = await self.controller.create_movie_postgres(
            self.mock_request
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), expected_response_data)

    async def test_create_movie_mongo(self):
        expected_response_data = {
            'data': 'Movie Created in Mongo DB Successfully'
        }

        self.controller.service.create_movie_mongo = AsyncMock(
            return_value={
                "data": expected_response_data["data"],
                "status_code": 201
            }
        )

        response = await self.controller.create_movie_mongo(self.mock_request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), expected_response_data)

    async def test_create_movie_external(self):
        expected_response_data = {
            'data': (
                'Movie Created Successfully in both Postgres & MongoDB '
                'from Redis DB Cache'
            )
        }

        self.controller.service.create_movie_external_from_cache = AsyncMock(
            return_value={
                "data": expected_response_data['data'],
                "status_code": 201
            }
        )

        response = await self.controller.create_movie_external(
            self.mock_request.title
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.body), expected_response_data)

    async def test_delete_movie_success(self):
        expected_response_data = {
            "data": "Movie Deleted Successfully Across all DB"
        }

        self.controller.service.delete_movie = AsyncMock(
            return_value={
                "data": expected_response_data["data"],
                "status_code": 200
            }
        )

        response = await self.controller.delete_movie("Inception")

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.body), expected_response_data)

    async def test_delete_movie_not_found(self):
        expected_response_data = {
            "data": "Movie not found in DB"
        }

        self.controller.service.delete_movie = AsyncMock(
            return_value={
                "data": expected_response_data["data"],
                "status_code": 501
            }
        )

        response = await self.controller.delete_movie("NonExistentMovie")

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 501)
        self.assertEqual(json.loads(response.body), expected_response_data)

    # def test_process_cpu_bound_tasks(self):
    #     expected_response_data = {
    #         'data': (
    #             'Successfully Processing Time & Resource Intense Task '
    #             'in the background....'
    #         )
    #     }

    #     self.controller.service.trigger_cpu_bound_task = MagicMock()

    #     response = self.controller.process_cpu_bound_tasks()

    #     self.controller.service.trigger_cpu_bound_task.assert_called_once()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.body), expected_response_data)


if __name__ == "__main__":
    unittest.main()
