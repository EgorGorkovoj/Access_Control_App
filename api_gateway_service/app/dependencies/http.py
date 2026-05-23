from fastapi import Request

from app.integrations.http.factory import HttpClientFactory


def get_http_factory(request: Request) -> HttpClientFactory:
    return HttpClientFactory(request)
