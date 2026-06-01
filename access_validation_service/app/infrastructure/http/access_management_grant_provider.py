import httpx
from app.application.dtos.access_request_event import TargetType
from app.domain.ports.exceptions import PermissionProviderHTTPError
from app.domain.ports.permission_grant_provider import IPermissionGrantProvider
from app.infrastructure.http.management_client import AccessManagementClient


class AccessManagementGrantProvider(IPermissionGrantProvider):
    def __init__(self, client: AccessManagementClient):
        self.client = client

    async def grant(
        self,
        user_id: int,
        target_type: TargetType,
        target_id: int,
    ) -> None:
        try:
            await self.client.post(
                '/api/v1/internal/permissions/grant',
                json={
                    'user_id': user_id,
                    'target_type': target_type.value,
                    'target_id': target_id,
                },
            )
        except httpx.RequestError as error:
            raise PermissionProviderHTTPError(
                f'Grant request failed (network error): user_id={user_id}, '
                f'target={target_type.value}:{target_id}, error={str(error)}'
            )

        except httpx.HTTPStatusError as error:
            raise PermissionProviderHTTPError(
                f'Grant request failed (HTTP {error.response.status_code}): '
                f'user_id={user_id}, target={target_type.value}:{target_id}'
            )
