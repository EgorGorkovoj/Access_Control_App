from app.application.dtos.user_permissions_dto import UserPermissionQueryDTO
from app.domain.repositories.group_access_repository import IGroupAccessRepository
from app.domain.repositories.user_access_repository import IUserAccessRepository
from app.domain.repositories.user_group_repository import IUserGroupRepository


class UserPermissionQueryService:
    def __init__(
        self,
        user_group_repo: IUserGroupRepository,
        group_access_repo: IGroupAccessRepository,
        user_access_repo: IUserAccessRepository,
    ):
        self.user_group_repo = user_group_repo
        self.group_access_repo = group_access_repo
        self.user_access_repo = user_access_repo

    async def get_all_user_permissions(self, user_id: int) -> UserPermissionQueryDTO:
        user_groups = await self.user_group_repo.get_all_by_user_id(user_id)
        group_accesses: set[int] = set()

        for group_id in user_groups:
            accesses = await self.group_access_repo.get_by_group_id(group_id)
            group_accesses.update(accesses)

        direct_accesses = await self.user_access_repo.get_all_user_accesses(user_id)
        all_accesses = group_accesses.union(direct_accesses)

        return UserPermissionQueryDTO(
            access_ids=list(all_accesses),
        )
