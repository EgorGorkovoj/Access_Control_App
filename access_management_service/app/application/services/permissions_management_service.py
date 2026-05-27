from app.application.exceptions.access import AccessNotFoundError
from app.application.exceptions.groups import GroupNotExistsError
from app.application.exceptions.user_access import (
    UserAlreadyHasAccessError,
    UserDoesNotHaveAccessError,
)
from app.application.exceptions.user_group import (
    UserGroupAlreadyExistsError,
    UserGroupNotFoundError,
)
from app.domain.models.access_request import TargetType
from app.domain.models.user_access import UserAccess
from app.domain.models.user_group import UserGroup
from app.domain.repositories.access_repository import IAccessRepository
from app.domain.repositories.group_repository import IRightGroupRepository
from app.domain.repositories.user_access_repository import (
    IUserAccessRepository,
)
from app.domain.repositories.user_group_repository import (
    IUserGroupRepository,
)


class PermissionManagementService:
    def __init__(
        self,
        user_group_repo: IUserGroupRepository,
        user_access_repo: IUserAccessRepository,
        group_repo: IRightGroupRepository,
        access_repo: IAccessRepository,
    ):
        self.user_group_repo = user_group_repo
        self.user_access_repo = user_access_repo
        self.group_repo = group_repo
        self.access_repo = access_repo

    async def grant_permissions(
        self,
        user_id: int,
        target_type: TargetType,
        target_id: int,
    ) -> None:
        """
        Granting a permission group or a single access right.
        """

        if target_type == TargetType.GROUP:
            await self._grant_group(user_id=user_id, group_id=target_id)
            return

        await self._grant_access(user_id=user_id, access_id=target_id)

    async def revoke_permission(
        self,
        user_id: int,
        target_type: TargetType,
        target_id: int,
    ) -> None:
        """
        Revoke a permission group or a single access right.
        """

        if target_type == TargetType.GROUP:
            await self._revoke_group(user_id=user_id, group_id=target_id)
            return
        await self._revoke_access(user_id=user_id, access_id=target_id)

    async def _grant_group(
        self,
        user_id: int,
        group_id: int,
    ) -> None:
        group = await self.group_repo.get_by_id(group_id)
        if not group:
            raise GroupNotExistsError(group_id)

        domain_model = UserGroup(
            user_id=user_id,
            group_id=group_id,
        )
        existing_group = await self.user_group_repo.get_user_group(domain_model)

        if existing_group:
            raise UserGroupAlreadyExistsError(
                user_id=user_id,
                group_id=group_id,
            )

        await self.user_group_repo.create(domain_model)

    async def _grant_access(
        self,
        user_id: int,
        access_id: int,
    ) -> None:
        access = await self.access_repo.get_by_id(access_id)
        if not access:
            raise AccessNotFoundError(access_id)

        existing_accesses = await self.user_access_repo.get_all_user_accesses(user_id)

        if access_id in existing_accesses:
            raise UserAlreadyHasAccessError(
                user_id=user_id,
                access_id=access_id,
            )

        domain_model = UserAccess(
            user_id=user_id,
            access_id=access_id,
        )

        await self.user_access_repo.add_access(domain_model)

    async def _revoke_group(
        self,
        user_id: int,
        group_id: int,
    ) -> None:
        domen_model = UserGroup(
            user_id=user_id,
            group_id=group_id,
        )

        existing_group = await self.user_group_repo.get_user_group(domen_model)

        if not existing_group:
            raise UserGroupNotFoundError(
                user_id=user_id,
                group_id=group_id,
            )

        await self.user_group_repo.delete(user_id, group_id)

    async def _revoke_access(
        self,
        user_id: int,
        access_id: int,
    ) -> None:
        existing_accesses = await self.user_access_repo.get_all_user_accesses(user_id)

        if access_id not in existing_accesses:
            raise UserDoesNotHaveAccessError(
                user_id=user_id,
                access_id=access_id,
            )

        await self.user_access_repo.remove_access(
            user_id=user_id,
            access_id=access_id,
        )
