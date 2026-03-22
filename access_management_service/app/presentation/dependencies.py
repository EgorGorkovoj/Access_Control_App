from fastapi import Depends

from app.application.services.access_service import AccessService
from app.application.services.group_access_service import GroupAccessService
from app.application.services.group_conflict_service import GroupConflictService
from app.application.services.resource_service import ResourceService
from app.application.services.right_group_service import RightGroupService
from app.infrastructure.database.dependencies import (
    get_access_service_impl,
    get_group_access_service_impl,
    get_group_conflict_service_impl,
    get_resource_service_impl,
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


def get_resource_service(
    service: ResourceService = Depends(get_resource_service_impl),
) -> ResourceService:
    return service


def get_access_service(service: AccessService = Depends(get_access_service_impl)) -> AccessService:
    return service


def get_group_access_service(
    service: GroupAccessService = Depends(get_group_access_service_impl),
) -> GroupAccessService:
    return service
