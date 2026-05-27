import httpx


class HttpClientRegistry:
    def __init__(self) -> None:
        self._clients: dict[str, httpx.AsyncClient] = {}

    def add(self, name: str, client: httpx.AsyncClient):
        self._clients[name] = client

    def get(self, name: str) -> httpx.AsyncClient:
        return self._clients[name]

    async def close(self) -> None:
        for client in self._clients.values():
            await client.aclose()
