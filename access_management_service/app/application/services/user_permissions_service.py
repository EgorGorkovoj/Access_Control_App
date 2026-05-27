from app.application.dtos.user_permissions_dto import UserPermissionsDTO
from app.domain.models.access_request import TargetType
from app.domain.repositories.group_conflict_repository import IGroupConflictRepository
from app.domain.repositories.user_group_repository import IUserGroupRepository


class UserPermissionsService:
    def __init__(
        self,
        user_group_repo: IUserGroupRepository,
        group_conflict_repo: IGroupConflictRepository,
    ):
        self.user_group_repo = user_group_repo
        self.group_conflict_repo = group_conflict_repo

    async def get_user_permissions(
        self,
        user_id: int,
        target_type: TargetType,
        target_id: int,
    ) -> UserPermissionsDTO:
        user_groups = await self.user_group_repo.get_all_by_user_id(user_id)

        if target_type == TargetType.GROUP:
            conflicting_groups = await self.group_conflict_repo.get_conflicting_group_ids(
                target_id
            )

            return UserPermissionsDTO(
                user_id=user_id,
                user_groups=user_groups,
                conflicting_groups=conflicting_groups,
            )

        conflicting_accesses = await self.group_conflict_repo.get_conflicting_accesses_for_groups(
            user_groups
        )

        return UserPermissionsDTO(
            user_id=user_id,
            user_groups=user_groups,
            conflicting_accesses=conflicting_accesses,
        )
