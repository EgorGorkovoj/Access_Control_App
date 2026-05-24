import httpx

from app.core.config import Config
from app.integrations.http.registry import HttpClientRegistry


def build_http_registry(settings: Config) -> HttpClientRegistry:
    registry = HttpClientRegistry()
    services = settings.services()

    registry.add('access_management', httpx.AsyncClient(base_url=services['access_management']))

    return registry
