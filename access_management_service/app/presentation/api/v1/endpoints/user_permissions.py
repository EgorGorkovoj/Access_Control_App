from fastapi import APIRouter, Depends, status

from app.application.services.permissions_management_service import PermissionManagementService
from app.application.services.user_permission_query_service import UserPermissionQueryService
from app.application.services.user_permissions_service import UserPermissionsService
from app.interface_adapters.dtos.grant_permissions import GrantPermissionsRequest
from app.interface_adapters.dtos.request import RevokeUserPermissionRequest
from app.interface_adapters.dtos.user_permissions import (
    UserAccessPermissionsResponse,
    UserPermissionsRequest,
    UserPermissionsResponse,
)
from app.presentation.dependencies import (
    get_permissions_management_service,
    get_user_permissions_query_service,
    get_user_permissions_service,
)

router = APIRouter()


@router.get('/users/{user_id}/permissions', status_code=status.HTTP_200_OK)
async def get_all_user_permissions(
    user_id: int,
    service: UserPermissionQueryService = Depends(get_user_permissions_query_service),
) -> UserAccessPermissionsResponse:
    """
    Returns all effective access permissions for a user.
    """
    permissions = await service.get_all_user_permissions(
        user_id=user_id,
    )
    return UserAccessPermissionsResponse.from_dto(permissions)


@router.post(
    '/internal/users/permissions', status_code=status.HTTP_200_OK, response_model_exclude_none=True
)
async def get_user_permissions(
    request: UserPermissionsRequest,
    service: UserPermissionsService = Depends(get_user_permissions_service),
) -> UserPermissionsResponse:
    dto = await service.get_user_permissions(
        user_id=request.user_id,
        target_type=request.target_type,
        target_id=request.target_id,
    )
    return UserPermissionsResponse.from_dto(dto=dto)


@router.post('/internal/permissions/grant', status_code=status.HTTP_201_CREATED)
async def grant_permissions_to_user(
    request: GrantPermissionsRequest,
    service: PermissionManagementService = Depends(get_permissions_management_service),
) -> None:
    await service.grant_permissions(
        user_id=request.user_id,
        target_type=request.target_type,
        target_id=request.target_id,
    )


@router.delete('/users/{user_id}/permissions', status_code=status.HTTP_204_NO_CONTENT)
async def revoke_user_permission(
    user_id: int,
    data: RevokeUserPermissionRequest,
    service: PermissionManagementService = Depends(get_permissions_management_service),
) -> None:
    await service.revoke_permission(
        user_id=user_id,
        target_type=data.target_type,
        target_id=data.target_id,
    )
