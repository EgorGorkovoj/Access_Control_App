from fastapi import Depends

from app.application.services.access_request_service import AccessRequestService
from app.application.services.access_service import AccessService
from app.application.services.group_access_service import GroupAccessService
from app.application.services.group_conflict_service import GroupConflictService
from app.application.services.permissions_management_service import PermissionManagementService
from app.application.services.resource_access_service import ResourceAccessService
from app.application.services.resource_service import ResourceService
from app.application.services.right_group_service import RightGroupService
from app.application.services.user_group_service import UserGroupService
from app.application.services.user_permission_query_service import UserPermissionQueryService
from app.application.services.user_permissions_service import UserPermissionsService
from app.infrastructure.database.dependencies import (
    get_access_request_service_impl,
    get_access_service_impl,
    get_group_access_service_impl,
    get_group_conflict_service_impl,
    get_permissions_management_service_impl,
    get_resource_access_service_impl,
    get_resource_service_impl,
    get_right_group_service_impl,
    get_user_group_service_impl,
    get_user_permissions_query_service_impl,
    get_user_permissions_service_impl,
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


def get_user_group_service(
    service: UserGroupService = Depends(get_user_group_service_impl),
) -> UserGroupService:
    return service


def get_request_service(
    service: AccessRequestService = Depends(get_access_request_service_impl),
) -> AccessRequestService:
    return service


def get_user_permissions_service(
    service: UserPermissionsService = Depends(get_user_permissions_service_impl),
) -> UserPermissionsService:
    return service


def get_permissions_management_service(
    service: PermissionManagementService = Depends(get_permissions_management_service_impl),
) -> PermissionManagementService:
    return service


def get_user_permissions_query_service(
    service: UserPermissionQueryService = Depends(get_user_permissions_query_service_impl),
) -> UserPermissionQueryService:
    return service


def get_resource_access_service(
    service: ResourceAccessService = Depends(get_resource_access_service_impl),
) -> ResourceAccessService:
    return service
