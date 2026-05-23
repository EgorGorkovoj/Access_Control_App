import httpx


class HttpClient:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def post(self, url: str, json: dict) -> dict:
        response = await self._client.post(url, json=json)
        response.raise_for_status()
        return response.json()

    async def get(self, url: str) -> dict:
        response = await self._client.get(url)
        response.raise_for_status()
        return response.json()
