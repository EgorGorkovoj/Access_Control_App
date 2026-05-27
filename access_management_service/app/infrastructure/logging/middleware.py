import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all HTTP requests."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        duration = time.time() - start_time
        logger.info(
            f'Request: {request.method} {request.url} - {duration:.3f} sec; '
            f'Response: {response.status_code}'
        )
        return response
