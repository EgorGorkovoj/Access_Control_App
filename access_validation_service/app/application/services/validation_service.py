from app.application.dtos.access_request_event import TargetType, ValidationRequestDTO
from app.application.dtos.user_permissions import UserPermissionsDTO
from app.application.exceptions.validation import (
    AccessConflictError,
    GroupConflictError,
)
from app.domain.models.request_status import RequestStatus
from app.domain.ports.permission_grant_provider import IPermissionGrantProvider
from app.domain.ports.permission_provider import IUserPermissionProvider
from app.domain.ports.request_status_updater import IRequestStatusUpdater


class ValidationService:
    def __init__(
        self,
        permission_provider: IUserPermissionProvider,
        status_updater: IRequestStatusUpdater,
        permission_grant_provider: IPermissionGrantProvider,
    ):
        self.permission_provider = permission_provider
        self.status_updater = status_updater
        self.permission_grant_provider = permission_grant_provider

    async def validate_request(self, dto: ValidationRequestDTO) -> None:
        await self.status_updater.update_status(dto.request_id, RequestStatus.IN_PROGRESS)
        try:
            permissions = await self.permission_provider.get_user_permissions(
                user_id=dto.user_id,
                target_type=dto.target_type,
                target_id=dto.target_id,
            )

            if dto.target_type == TargetType.GROUP:
                self._validate_group_request(
                    dto=dto,
                    permissions=permissions,
                )
            else:
                self._validate_access_request(
                    dto=dto,
                    permissions=permissions,
                )
            await self.status_updater.update_status(
                request_id=dto.request_id, status=RequestStatus.APPROVED
            )
            await self.permission_grant_provider.grant(
                user_id=dto.user_id,
                target_type=dto.target_type,
                target_id=dto.target_id,
            )
        except (GroupConflictError, AccessConflictError):
            await self.status_updater.update_status(
                request_id=dto.request_id,
                status=RequestStatus.REJECTED,
            )
            return

    def _validate_group_request(
        self,
        dto: ValidationRequestDTO,
        permissions: UserPermissionsDTO,
    ) -> None:
        """
        Проверка выдачи группы.
        """

        user_groups = set(permissions.user_groups or [])

        conflicting_groups = set(permissions.conflicting_groups or [])

        if user_groups & conflicting_groups:
            raise GroupConflictError(
                dto.user_id,
                dto.target_id,
            )

    def _validate_access_request(
        self,
        dto: ValidationRequestDTO,
        permissions: UserPermissionsDTO,
    ) -> None:
        """
        Проверка выдачи отдельного доступа.
        """

        conflicting_accesses = set(permissions.conflicting_accesses or [])

        if dto.target_id in conflicting_accesses:
            raise AccessConflictError(
                dto.user_id,
                dto.target_id,
            )
