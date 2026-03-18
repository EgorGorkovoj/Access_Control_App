from abc import ABC, abstractmethod
from typing import Sequence

from app.domain.models.right_group import RightGroup


class IRightGroupRepository(ABC):
    @abstractmethod
    async def get_by_id(self, group_id: int) -> RightGroup | None:
        pass

    @abstractmethod
    async def get_all(self, limit: int | None, offset: int) -> Sequence[RightGroup]:
        pass

    @abstractmethod
    async def get_by_name(self, group_name: str):
        pass

    @abstractmethod
    async def create(self, group: RightGroup) -> RightGroup:
        pass

    @abstractmethod
    async def update(self, group: RightGroup) -> RightGroup | None:
        pass

    @abstractmethod
    async def delete(self, group_id: int) -> bool:
        pass
