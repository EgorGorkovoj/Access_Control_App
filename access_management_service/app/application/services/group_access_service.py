from app.application.dtos.group_access_dto import GroupAccessDTO
from app.application.exceptions.access import AccessNotFoundError
from app.application.exceptions.group_access import (
    GroupAccessAlreadyExistsError,
    GroupAccessNotFoundError,
)
from app.application.exceptions.groups import GroupNotExistsError
from app.domain.models.group_access import GroupAccess
from app.domain.repositories.access_repository import IAccessRepository
from app.domain.repositories.group_access_repository import IGroupAccessRepository
from app.domain.repositories.group_repository import IRightGroupRepository


class GroupAccessService:
    def __init__(
        self,
        group_access_repo: IGroupAccessRepository,
        group_repo: IRightGroupRepository,
        access_repo: IAccessRepository,
    ):
        self.group_access_repo = group_access_repo
        self.group_repo = group_repo
        self.access_repo = access_repo

    async def add_access_to_group(self, group_id: int, access_id: int) -> GroupAccessDTO:
        group = await self.group_repo.get_by_id(group_id)
        if not group:
            raise GroupNotExistsError(group_id)

        access = await self.access_repo.get_by_id(access_id)
        if not access:
            raise AccessNotFoundError(access_id)

        exists = await self.group_access_repo.exists(group_id, access_id)
        if exists:
            raise GroupAccessAlreadyExistsError(group_id, access_id)

        relation = GroupAccess(group_id=group_id, access_id=access_id)

        created = await self.group_access_repo.create(relation)

        return GroupAccessDTO(group_id=created.group_id, access_id=created.access_id)

    async def remove_access_from_group(self, group_id: int, access_id: int) -> None:
        deleted = await self.group_access_repo.delete(group_id, access_id)

        if not deleted:
            raise GroupAccessNotFoundError(group_id, access_id)

    async def get_group_accesses(self, group_id: int) -> list[int]:
        group = await self.group_repo.get_by_id(group_id)
        if not group:
            raise GroupNotExistsError(group_id)

        return await self.group_access_repo.get_by_group_id(group_id)
