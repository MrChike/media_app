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

    @patch('movies.service.fetch_movie_omdb')
    def test_get_movie_details_success(self, mock_fetch):
        """Test successful retrieval of movie details."""
        # Create a mock response for fetch_movie_omdb
        mock_response = {
            "Title": "Inception",
            "Year": "2010",
            "Actors": "Leonardo DiCaprio, Joseph Gordon-Levitt",
        }

        # Mock the successful fetch response
        mock_fetch.return_value = mock_response

        # Create a test MovieSchema input
        test_movie = MovieSchema(title="Inception", actors="Leonardo DiCaprio")

        # Call the service method
        response = asyncio.run(self.service.get_movie_details(test_movie))

        # Validate the response
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["data"], mock_response)
        mock_fetch.assert_called_once()

    @patch('movies.service.fetch_movie_omdb')
    @patch('movies.service.logger')
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
        self.assertEqual(
            response["data"],
            (
                "Sorry, we couldn't fetch the movie details right now. "
                "Please try again later."
            )
        )

        # Check that logging error is called
        mock_logger.error.assert_called_with(
            "Failed to fetch movie details: OMDB API failure"
        )

    @patch('movies.service.fetch_movie_omdb')
    @patch('movies.service.logger')
    def test_get_movie_details_failure_with_status_code(
        self, mock_logger, mock_fetch
    ):
        """
        Test failure when an exception occurs during the fetch
        and the exception has a response with a status_code.
        """
        # Simulate an exception with a response containing a status_code
        mock_exception = Exception("OMDB API failure")
        mock_exception.response = MagicMock()  # type: ignore
        # Simulating a 502 Bad Gateway error
        mock_exception.response.status_code = 502  # type: ignore

        # Set the mock to raise this exception
        mock_fetch.side_effect = mock_exception

        # Create a test MovieSchema input
        test_movie = MovieSchema(title="Inception", actors="Leonardo DiCaprio")

        # Call the service method
        response = asyncio.run(self.service.get_movie_details(test_movie))

        # Validate the response
        self.assertEqual(
            response["status_code"], 502
        )  # Check if status_code is 502
        self.assertEqual(
            response["data"],
            (
                "Sorry, we couldn't fetch the movie details right now. "
                "Please try again later."
            )
        )

        # Check that logging error is called
        mock_logger.error.assert_called_with(
            "Failed to fetch movie details: OMDB API failure"
        )


# Run the tests
if __name__ == "__main__":
    unittest.main()
