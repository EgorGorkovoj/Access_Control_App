import httpx


class AccessManagementClient:
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url
        self.timeout = timeout
        self.client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def stop(self) -> None:
        if self.client:
            await self.client.aclose()

    async def post(self, path: str, json: dict) -> httpx.Response:
        if self.client is None:
            raise RuntimeError('Client not started')

        response = await self.client.post(path, json=json)
        response.raise_for_status()
        return response

    async def patch(self, path: str, json: dict) -> httpx.Response:
        if self.client is None:
            raise RuntimeError('Client not started')

        response = await self.client.patch(path, json=json)
        response.raise_for_status()
        return response
