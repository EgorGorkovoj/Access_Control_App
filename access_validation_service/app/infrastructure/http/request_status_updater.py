from app.domain.models.request_status import RequestStatus
from app.domain.ports.request_status_updater import (
    IRequestStatusUpdater,
)
from app.infrastructure.http.management_client import (
    AccessManagementClient,
)


class AccessManagementRequestStatusUpdater(IRequestStatusUpdater):
    def __init__(self, client: AccessManagementClient):
        self.client = client

    async def update_status(self, request_id: str, status: RequestStatus) -> None:
        await self.client.patch(
            f'/api/v1/request/{request_id}/update-status',
            json={
                'status': status.value,
            },
        )
