from app.application.dtos.user_group_dto import UserGroupDTO
from app.application.exceptions.groups import GroupNotExistsError
from app.application.exceptions.user_group import (
    UserGroupAlreadyExistsError,
    UserGroupNotFoundError,
)
from app.domain.models.user_group import UserGroup
from app.domain.repositories.group_repository import IRightGroupRepository
from app.domain.repositories.user_group_repository import IUserGroupRepository


class UserGroupService:
    def __init__(self, user_group_repo: IUserGroupRepository, group_repo: IRightGroupRepository):
        self.user_group_repo = user_group_repo
        self.group_repo = group_repo

    async def add_user_to_group(self, user_id: int, group_id: int) -> UserGroupDTO:
        group = await self.group_repo.get_by_id(group_id)
        if not group:
            raise GroupNotExistsError(group_id)

        exists = await self.user_group_repo.exists(user_id, group_id)
        if exists:
            raise UserGroupAlreadyExistsError(user_id, group_id)

        domain_model = UserGroup(user_id=user_id, group_id=group_id)
        created_user_group = await self.user_group_repo.create(domain_model)

        return UserGroupDTO(
            user_id=created_user_group.user_id, group_id=created_user_group.group_id
        )

    async def remove_user_from_group(self, user_id: int, group_id: int) -> None:
        deleted = await self.user_group_repo.delete(user_id, group_id)

        if not deleted:
            raise UserGroupNotFoundError(user_id, group_id)

    async def get_user_groups_ids(self, user_id: int) -> list[int]:
        return await self.user_group_repo.get_all_by_user_id(user_id)
