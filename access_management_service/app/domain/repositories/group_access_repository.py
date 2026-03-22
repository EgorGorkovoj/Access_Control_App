from abc import ABC, abstractmethod

from app.domain.models.group_access import GroupAccess


class IGroupAccessRepository(ABC):
    @abstractmethod
    async def create(self, group_access: GroupAccess) -> GroupAccess:
        pass

    @abstractmethod
    async def exists(self, group_id: int, access_id: int) -> bool:
        pass

    @abstractmethod
    async def delete(self, group_id: int, access_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_group_id(self, group_id: int) -> list[GroupAccess]:
        pass
