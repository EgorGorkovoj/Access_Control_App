from fastapi import APIRouter

from app.presentation.api.v1.endpoints import right_group__router

main_router = APIRouter(prefix='/api/v1')

main_router.include_router(right_group__router, tags=['Right Group'])
