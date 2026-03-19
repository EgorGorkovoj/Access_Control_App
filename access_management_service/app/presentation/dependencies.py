from fastapi import Depends

from app.application.services.group_conflict_service import GroupConflictService
from app.application.services.right_group_service import RightGroupService
from app.infrastructure.database.dependencies import (
    get_group_conflict_service_impl,
    get_right_group_service_impl,
)


def get_right_group_service(
    service: RightGroupService = Depends(get_right_group_service_impl),
) -> RightGroupService:
    return service


def get_right_group_conflict_service(
    service: GroupConflictService = Depends(get_group_conflict_service_impl),
) -> GroupConflictService:
    return service
