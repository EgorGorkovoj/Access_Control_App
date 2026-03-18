from fastapi import FastAPI

from app.infrastructure.config.settings import settings
from app.infrastructure.logging.config import setup_logging
from app.infrastructure.logging.middleware import LoggingMiddleware
from app.presentation.api.v1.exception_handlers import register_exception_handlers
from app.presentation.api.v1.routers import main_router

setup_logging()

app = FastAPI(
    title='Access Management Service',
    description='Сервис с работой и управлением доступами к ресурсам',
    debug=settings.DEBUG,
)

register_exception_handlers(app=app)

app.add_middleware(LoggingMiddleware)
app.include_router(main_router)
