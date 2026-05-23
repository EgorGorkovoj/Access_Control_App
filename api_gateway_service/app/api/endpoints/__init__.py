from app.api.endpoints.proxy_access_management_server import access_router
from app.api.endpoints.request import router as request_router

__all__ = [
    'access_router',
    'request_router',
]
