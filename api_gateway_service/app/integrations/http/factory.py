from fastapi import Request

from app.integrations.http.client import HttpClient


class HttpClientFactory:
    def __init__(self, request: Request):
        self._registry = request.app.state.http_registry

    def access_management(self) -> HttpClient:
        return HttpClient(self._registry.get('access_management'))
