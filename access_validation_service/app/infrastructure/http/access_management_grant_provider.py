from app.application.dtos.access_request_event import TargetType
from app.domain.ports.permission_grant_provider import IPermissionGrantProvider
from app.infrastructure.http.management_client import AccessManagementClient


class AccessManagementGrantProvider(IPermissionGrantProvider):
    def __init__(
        self,
        client: AccessManagementClient,
    ):
        self.client = client

    async def grant(
        self,
        user_id: int,
        target_type: TargetType,
        target_id: int,
    ) -> None:
        await self.client.post(
            'api/v1/internal/permissions/grant',
            json={
                'user_id': user_id,
                'target_type': target_type.value,
                'target_id': target_id,
            },
        )
