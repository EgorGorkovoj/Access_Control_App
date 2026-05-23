from fastapi import APIRouter

from app.api.endpoints import access_router, request_router

main_router = APIRouter()

main_router.include_router(
    access_router, tags=['Access Management Service'], include_in_schema=False
)
main_router.include_router(request_router, tags=['Requests'])
