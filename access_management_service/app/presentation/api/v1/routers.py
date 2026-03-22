from fastapi import APIRouter

from app.presentation.api.v1.endpoints import (
    access_router,
    group_access_router,
    group_conflict_router,
    resource_router,
    right_group_router,
)

main_router = APIRouter(prefix='/api/v1')

main_router.include_router(right_group_router, tags=['Right Group'])
main_router.include_router(group_conflict_router, tags=['Group Conflict'])
main_router.include_router(resource_router, tags=['Resource'])
main_router.include_router(access_router, tags=['Access'])
main_router.include_router(group_access_router, tags=['Group Access'])
