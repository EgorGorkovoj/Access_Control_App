from sqlalchemy.exc import IntegrityError

from app.application.dtos.group_conflict_dto import GroupConflictDTO
from app.application.exceptions.group_conflict import (
    GroupConflictAlreadyExistsError,
    GroupConflictNotFoundError,
    GroupConflictWithItselfError,
)
from app.application.exceptions.groups import GroupNotExistsError
from app.domain.models.group_conflict import GroupConflict
from app.domain.repositories.group_conflict_repository import IGroupConflictRepository
from app.domain.repositories.group_repository import IRightGroupRepository


class GroupConflictService:
    def __init__(self, conflict_repo: IGroupConflictRepository, group_repo: IRightGroupRepository):
        self.conflict_repo = conflict_repo
        self.group_repo = group_repo

    async def get_conflicting_group_ids(self, group_id: int) -> list[int]:
        existing_group = await self.group_repo.get_by_id(group_id)
        if not existing_group:
            raise GroupNotExistsError(group_id)

        return await self.conflict_repo.get_conflicting_group_ids(group_id)

    async def add_group_conflict(
        self, group_id: int, conflicting_group_id: int
    ) -> GroupConflictDTO:
        if group_id == conflicting_group_id:
            raise GroupConflictWithItselfError(group_id)

        conflict = GroupConflict(group_id=group_id, conflict_group_id=conflicting_group_id)

        try:
            created = await self.conflict_repo.create(conflict)
        except IntegrityError:
            raise GroupConflictAlreadyExistsError(group_id, conflicting_group_id)

        return GroupConflictDTO(
            group_id=created.group_id, conflict_group_id=created.conflict_group_id
        )

    async def remove_group_conflict(self, group_id: int, conflicting_group_id: int) -> None:
        conflict = GroupConflict(group_id=group_id, conflict_group_id=conflicting_group_id)

        deleted = await self.conflict_repo.delete(conflict)

        if not deleted:
            raise GroupConflictNotFoundError(group_id, conflicting_group_id)
