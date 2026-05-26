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
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class ValidationService:
    """
    Application service responsible for validating access requests.
    The service validates whether a requested permission may be granted
    without violating access conflict rules.
    Request lifecycle:
        PENDING -> IN_PROGRESS -> APPROVED / REJECTED
    Validation flow:
    1. Mark request as IN_PROGRESS.
    2. Retrieve user's current permissions and conflict information.
    3. Validate requested target:
        - group requests -> check conflicting groups
        - access requests -> check conflicting accesses
    4. If validation succeeds:
        - grant permission
        - mark request as APPROVED
    5. If a conflict is detected:
        - mark request as REJECTED
    """

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
        """
        Validate and process an access request.
        The request is first moved to IN_PROGRESS state. Validation rules
        depend on requested target type.
        Group requests are validated against user's existing groups and
        their conflicts.
        Access requests are validated against accesses conflicting with
        user's current permissions.
        If validation passes, permission is granted and request is approved.
        Otherwise, request is rejected.
        """
        logger.info(
            'Starting validation: request_id=%s user_id=%s target=%s:%s',
            dto.request_id,
            dto.user_id,
            dto.target_type.value,
            dto.target_id,
        )
        await self.status_updater.update_status(
            dto.request_id,
            RequestStatus.IN_PROGRESS,
        )

        permissions = await self.permission_provider.get_user_permissions(
            user_id=dto.user_id,
            target_type=dto.target_type,
            target_id=dto.target_id,
        )

        try:
            self._validate(dto, permissions)

        except (GroupConflictError, AccessConflictError):
            logger.warning(
                'Validation rejected: request_id=%s conflict detected',
                dto.request_id,
            )
            await self._reject(dto.request_id)
            return

        await self.permission_grant_provider.grant(
            user_id=dto.user_id,
            target_type=dto.target_type,
            target_id=dto.target_id,
        )

        await self._approve(dto.request_id)
        logger.info(
            'Validation approved: request_id=%s',
            dto.request_id,
        )

    def _validate(
        self,
        dto: ValidationRequestDTO,
        permissions: UserPermissionsDTO,
    ) -> None:
        """
        Dispatch validation according to requested target type.
        Group requests are validated against conflicting groups.
        Individual access requests are validated against conflicting
        accesses.
        Raises:
            GroupConflictError:
                If requested group conflicts with user's current groups.
            AccessConflictError:
                If requested access conflicts with user's existing
                permissions.
        """

        if dto.target_type == TargetType.GROUP:
            self._validate_group_request(dto, permissions)
        else:
            self._validate_access_request(dto, permissions)

    async def _approve(self, request_id: str) -> None:
        await self.status_updater.update_status(
            request_id,
            RequestStatus.APPROVED,
        )

    async def _reject(self, request_id: str) -> None:
        await self.status_updater.update_status(
            request_id,
            RequestStatus.REJECTED,
        )

    def _validate_group_request(
        self,
        dto: ValidationRequestDTO,
        permissions: UserPermissionsDTO,
    ) -> None:
        """
        Validate granting of a permission group.
        Validation compares user's current groups with groups conflicting
        with the requested group.
        A conflict exists when at least one of the user's assigned groups
        appears in the requested group's conflict set.
        Raises:
            GroupConflictError:
                If requested group conflicts with an already assigned
                group.
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
        Validate granting of an individual access.
        Validation checks whether requested access is present in the set
        of accesses conflicting with user's current permissions.
        Raises:
            AccessConflictError:
                If requested access conflicts with user's existing access
                set.
        """

        conflicting_accesses = set(permissions.conflicting_accesses or [])

        if dto.target_id in conflicting_accesses:
            raise AccessConflictError(
                dto.user_id,
                dto.target_id,
            )
