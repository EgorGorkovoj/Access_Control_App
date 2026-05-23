from app.application.dtos.access_request_event import TargetType
from app.application.dtos.user_permissions import UserPermissionsDTO
from app.domain.ports.permission_provider import IUserPermissionProvider
from app.infrastructure.http.management_client import AccessManagementClient


class AccessManagementPermissionProvider(IUserPermissionProvider):
    def __init__(self, client: AccessManagementClient):
        self.client = client

    async def get_user_permissions(
        self,
        user_id: int,
        target_type: TargetType,
        target_id: int,
    ) -> UserPermissionsDTO:
        response = await self.client.post(
            'api/v1/internal/users/permissions',
            json={
                'user_id': user_id,
                'target_type': target_type,
                'target_id': target_id,
            },
        )

        data = response.json()

        return UserPermissionsDTO(
            user_id=data['user_id'],
            user_accesses=data['user_accesses'],
            user_groups=data.get('user_groups'),
            accesses_destination_group=data.get('accesses_destination_group'),
            conflicting_groups=data.get('conflicting_groups'),
        )
