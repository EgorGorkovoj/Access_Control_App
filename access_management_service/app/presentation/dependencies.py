from fastapi import Depends

from app.application.services.right_group_service import RightGroupService
from app.infrastructure.database.dependencies import get_right_group_service_impl


def get_right_group_service(
    service: RightGroupService = Depends(get_right_group_service_impl),
) -> RightGroupService:
    return service
