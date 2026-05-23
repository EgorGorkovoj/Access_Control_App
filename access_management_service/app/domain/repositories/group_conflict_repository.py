from abc import ABC, abstractmethod

from app.domain.models.group_conflict import GroupConflict


class IGroupConflictRepository(ABC):
    # @abstractmethod
    # async def get_by_group_id(self, group_conflict_id: int) -> Sequence[GroupConflict]:
    #     pass
    @abstractmethod
    async def get_conflicting_group_ids(self, group_id: int) -> list[int]:
        pass

    @abstractmethod
    async def get_conflicting_accesses_for_groups(self, group_ids: list[int]) -> list[int]:
        pass

    @abstractmethod
    async def create(self, group_conflict: GroupConflict) -> GroupConflict:
        pass

    @abstractmethod
    async def delete(self, group_conflict: GroupConflict) -> bool:
        pass
