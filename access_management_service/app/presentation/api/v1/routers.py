from fastapi import APIRouter

from app.presentation.api.v1.endpoints import group_conflict_router, right_group_router

main_router = APIRouter(prefix='/api/v1')

main_router.include_router(right_group_router, tags=['Right Group'])
main_router.include_router(group_conflict_router, tags=['Group Conflict'])
