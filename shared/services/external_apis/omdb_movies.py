import httpx
import logging

logger = logging.getLogger(__name__)

async def fetch_movie_omdb(request_url: str):
    """
    Asynchronously makes a request to the OMDB API.

    - Logs and raises HTTP, network, and unexpected errors.
    - Focuses on reliable API calls and low-level error reporting.
    - Leaves user-facing error handling to the caller.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(request_url)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Unexpected error in fetch_movie_omdb: {e}")
        raise
