import httpx
from app.domain.models.request_status import RequestStatus
from app.domain.ports.request_status_updater import IRequestStatusUpdater
from app.infrastructure.http.exceptions import PermissionProviderHTTPError
from app.infrastructure.http.management_client import AccessManagementClient


class AccessManagementRequestStatusUpdater(IRequestStatusUpdater):
    def __init__(self, client: AccessManagementClient):
        self.client = client

    async def update_status(self, request_id: str, status: RequestStatus) -> None:
        try:
            await self.client.patch(
                f'/api/v1/request/{request_id}/update-status',
                json={
                    'status': status.value,
                },
            )
        except httpx.RequestError as error:
            raise PermissionProviderHTTPError(
                'Failed to update request status (network error): '
                f'request_id={request_id}, error={str(error)}'
            )
        except httpx.HTTPStatusError as error:
            raise PermissionProviderHTTPError(
                f'Failed to update request status (HTTP {error.response.status_code}): '
                f'request_id={request_id}'
            )
