from app.presentation.api.v1.endpoints.accesses import router as access_router
from app.presentation.api.v1.endpoints.group_accesses import router as group_access_router
from app.presentation.api.v1.endpoints.group_conflicts import router as group_conflict_router
from app.presentation.api.v1.endpoints.requests import router as request_router
from app.presentation.api.v1.endpoints.resources import router as resource_router
from app.presentation.api.v1.endpoints.right_groups import router as right_group_router
from app.presentation.api.v1.endpoints.user_groups import router as user_group_router
from app.presentation.api.v1.endpoints.user_permissions import router as user_permissions_router

__all__ = [
    'right_group_router',
    'group_conflict_router',
    'resource_router',
    'access_router',
    'group_access_router',
    'user_group_router',
    'request_router',
    'user_permissions_router',
]
