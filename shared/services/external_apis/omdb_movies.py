import httpx

async def fetch_movie_omdb(request_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(request_url)
        return response.json()
