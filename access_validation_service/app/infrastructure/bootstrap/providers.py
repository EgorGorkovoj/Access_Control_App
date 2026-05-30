from app.application.services.validation_service import (
    ValidationService,
)
from app.infrastructure.http.access_management_grant_provider import (
    AccessManagementGrantProvider,
)
from app.infrastructure.http.access_management_permission_provider import (
    AccessManagementPermissionProvider,
)
from app.infrastructure.http.management_client import AccessManagementClient
from app.infrastructure.http.request_status_updater import (
    AccessManagementRequestStatusUpdater,
)


def get_validation_service(client: AccessManagementClient) -> ValidationService:
    permission_provider = AccessManagementPermissionProvider(client)
    status_updater = AccessManagementRequestStatusUpdater(client)
    permission_grant_provider = AccessManagementGrantProvider(client)
    return ValidationService(
        permission_provider=permission_provider,
        status_updater=status_updater,
        permission_grant_provider=permission_grant_provider,
    )
