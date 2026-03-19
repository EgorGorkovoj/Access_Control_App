from abc import ABC, abstractmethod
from typing import Sequence

from app.domain.models.group_conflict import GroupConflict


class IGroupConflictRepository(ABC):
    @abstractmethod
    async def get_by_group_id(self, group_conflict_id: int) -> Sequence[GroupConflict]:
        pass

    @abstractmethod
    async def create(self, group_conflict: GroupConflict) -> GroupConflict:
        pass

    @abstractmethod
    async def delete(self, group_conflict: GroupConflict) -> bool:
        pass
