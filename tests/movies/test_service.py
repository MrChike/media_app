import unittest
from unittest.mock import patch, MagicMock
from movies.service import MovieService
from movies.schema import MovieSchema
import asyncio

class TestMovieService(unittest.TestCase):
    def setUp(self):
        """Setup test environment before each test."""
        # Initialize MovieService
        self.service = MovieService()

    @patch('movies.service.fetch_movie_omdb')  # Mock the external fetch function
    def test_get_movie_details_success(self, mock_fetch):
        """Test successful retrieval of movie details."""
        # Create a mock response for fetch_movie_omdb
        mock_response = {
            "Title": "Inception",
            "Year": "2010",
            "Actors": "Leonardo DiCaprio, Joseph Gordon-Levitt",
        }
        mock_fetch.return_value = mock_response  # Mock the successful fetch response

        # Create a test MovieSchema input
        test_movie = MovieSchema(title="Inception", actors="Leonardo DiCaprio")

        # Call the service method
        response = asyncio.run(self.service.get_movie_details(test_movie))

        # Validate the response
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["data"], mock_response)
        mock_fetch.assert_called_once()  # Ensure fetch was called once with the correct URL

    @patch('movies.service.fetch_movie_omdb')  # Mock the external fetch function
    @patch('movies.service.logger')  # Mock the logger to check if error logging happens
    def test_get_movie_details_failure(self, mock_logger, mock_fetch):
        """Test failure when an exception occurs during the fetch."""
        # Simulate an exception being raised in fetch_movie_omdb
        mock_fetch.side_effect = Exception("OMDB API failure")

        # Create a test MovieSchema input
        test_movie = MovieSchema(title="Inception", actors="Leonardo DiCaprio")

        # Call the service method
        response = asyncio.run(self.service.get_movie_details(test_movie))

        # Validate the response
        self.assertEqual(response["status_code"], 503)
        self.assertEqual(response["data"], "Sorry, we couldn't fetch the movie details right now. Please try again later.")
        
        # Check that logging error is called
        mock_logger.error.assert_called_with("Failed to fetch movie details: OMDB API failure")


# Run the tests
if __name__ == "__main__":
    unittest.main()
