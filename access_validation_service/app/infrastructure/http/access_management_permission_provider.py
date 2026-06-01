import httpx
from app.application.dtos.access_request_event import TargetType
from app.application.dtos.user_permissions import UserPermissionsDTO
from app.domain.ports.exceptions import (
    PermissionProviderHTTPError,
    PermissionProviderResponseError,
)
from app.domain.ports.permission_provider import IUserPermissionProvider
from app.infrastructure.http.management_client import AccessManagementClient


class AccessManagementPermissionProvider(IUserPermissionProvider):
    def __init__(self, client: AccessManagementClient):
        self.client = client

    async def get_user_permissions(
        self, user_id: int, target_type: TargetType, target_id: int
    ) -> UserPermissionsDTO:
        try:
            response = await self.client.post(
                '/api/v1/internal/users/permissions',
                json={
                    'user_id': user_id,
                    'target_type': target_type.value,
                    'target_id': target_id,
                },
            )
        except httpx.RequestError as error:
            raise PermissionProviderHTTPError(
                f'AccessManagement request failed: HTTP {error.response.status_code}'
            )
        try:
            data = response.json()
        except ValueError as error:
            raise PermissionProviderResponseError(
                f'AccessManagement returned invalid JSON: {str(error)}'
            )
        return UserPermissionsDTO(
            user_id=data['user_id'],
            user_groups=data.get('user_groups'),
            conflicting_groups=data.get('conflicting_groups'),
            conflicting_accesses=data.get('conflicting_accesses'),
        )
