from app.application.dtos.user_permissions_dto import UserPermissionsDTO

# from app.domain.repositories.group_access_repository import IGroupAccessRepository
from app.domain.models.access_request import TargetType
from app.domain.repositories.group_conflict_repository import IGroupConflictRepository

# from app.domain.repositories.user_access_repository import IUserAccessRepository
from app.domain.repositories.user_group_repository import IUserGroupRepository


class UserPermissionsService:
    def __init__(
        self,
        user_group_repo: IUserGroupRepository,
        group_conflict_repo: IGroupConflictRepository,
        # user_access_repo: IUserAccessRepository
    ):
        self.user_group_repo = user_group_repo
        self.group_conflict_repo = group_conflict_repo
        # self.user_access_repo = user_access_repo

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

    # async def revoke_permission(
    #     self,
    #     user_id: int,
    #     target_type: TargetType,
    #     target_id: int,
    # ) -> None:

    #     if target_type == TargetType.GROUP:
    #         await self.user_group_repo.delete(
    #             user_id=user_id,
    #             group_id=target_id,
    #         )
    #         return

    #     await self.user_access_repo.remove_access(
    #         user_id=user_id,
    #         access_id=target_id,
    #     )


# class UserPermissionsService:
#     def __init__(
#         self,
#         user_group_repo: IUserGroupRepository,
#         user_access_repo: IUserAccessRepository,
#         group_access_repo: IGroupAccessRepository,
#         group_conflict_repo: IGroupConflictRepository
#     ):
#         self.user_group_repo = user_group_repo
#         self.user_access_repo = user_access_repo
#         self.group_access_repo = group_access_repo
#         self.group_conflict_repo = group_conflict_repo

#     async def get_user_permissions(
#             self, user_id: int, target_type: TargetType, target_id: int
#     ) -> UserPermissionsDTO:
#         user_accesses = await self.user_access_repo.get_all_user_accesses(user_id)
#         if target_type == TargetType.GROUP:
#             user_groups = await self.user_group_repo.get_by_user_id(user_id)
#             group_accesses = await self.group_access_repo.get_by_group_id(target_id)
#             group_conflicts = await self.group_conflict_repo.get_conflicting_group_ids(target_id)
#             return UserPermissionsDTO(
#                 user_id=user_id,
#                 user_accesses=user_accesses,
#                 user_groups=user_groups,
#                 accesses_destination_group=group_accesses,
#                 conflicting_groups=group_conflicts
#             )
#         return UserPermissionsDTO(
#             user_id=user_id,
#             user_accesses=user_accesses,
#             accesses_destination_group=[target_id]
#         )
