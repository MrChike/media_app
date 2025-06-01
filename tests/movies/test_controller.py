import unittest
import asyncio
import json
from unittest.mock import MagicMock
from movies.controller import MovieController
from movies.schema import MovieSchema
from fastapi.responses import JSONResponse
from movies.service import MovieService


class TestMovieController(unittest.TestCase):

    def setUp(self):
        """Setup test environment before each test."""
        # Create a mock for MovieService
        self.mock_service = MagicMock(spec=MovieService)
        
        # Initialize MovieController with the mocked service
        self.controller = MovieController()
        self.controller.service = self.mock_service
        
    def test_get_movie_success(self):
        """Test successful movie retrieval."""
        # Create a mock response from the service
        mock_response = {
            "status_code": 200,
            "data": {"title": "Inception", "actors": "Leonardo DiCaprio, Joseph Gordon-Levitt"}
        }
        
        # Mock the service's get_movie_details method to return the mock response
        self.mock_service.get_movie_details.return_value = mock_response
        
        # Create a test movie schema input (this simulates the input data)
        test_movie = MovieSchema(title="Inception", actors="Leonardo DiCaprio")
        
        # Call the controller method (simulate POST request)
        response = asyncio.run(self.controller.get_movie(test_movie))
        
        # Validate the response
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 200)
        import json
        self.assertEqual(json.loads(response.body), {"data": mock_response["data"]})  # Check the response body


    def test_get_movie_failure(self):
        """Test movie retrieval failure scenario."""
        # Create a mock failure response from the service
        mock_response = {
            "status_code": 503,
            "data": "Sorry, we couldn't fetch the movie details right now. Please try again later."
        }
        
        # Mock the service's get_movie_details method to return the failure response
        self.mock_service.get_movie_details.return_value = mock_response
        
        # Create a test movie schema input
        test_movie = MovieSchema(title="Unknown Movie", actors="Unknown Actor")

        # Call the controller method (simulate POST request)
        response = asyncio.run(self.controller.get_movie(test_movie))

        # Validate the response
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(json.loads(response.body), {"data": mock_response["data"]})
        self.assertEqual(json.loads(response.body), {"data": mock_response["data"]})
        self.assertEqual(json.loads(response.body), {"data": mock_response["data"]})

# Run the tests
if __name__ == "__main__":
    unittest.main()
