from app.presentation.api.v1.endpoints.group_conflicts import router as group_conflict_router
from app.presentation.api.v1.endpoints.right_groups import router as right_group_router

__all__ = [
    'right_group_router',
    'group_conflict_router',
]
