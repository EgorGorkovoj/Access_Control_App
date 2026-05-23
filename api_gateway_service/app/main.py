from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.logging.config import setup_logging
from app.core.logging.middleware import LoggingMiddleware
from app.integrations.http.builder import build_http_registry
from app.kafka.producer import producer_client

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await producer_client.start()
    app.state.http_registry = build_http_registry(settings=settings)

    try:
        yield
    finally:
        await producer_client.stop()
        await app.state.http_registry.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(LoggingMiddleware)
app.include_router(main_router)
