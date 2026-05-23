from abc import ABC, abstractmethod

from app.domain.models.user_group import UserGroup


class IUserGroupRepository(ABC):
    @abstractmethod
    async def create(self, relation: UserGroup) -> UserGroup:
        pass

    @abstractmethod
    async def exists(self, user_id: int, group_id: int) -> bool:
        pass

    @abstractmethod
    async def delete(self, user_id: int, group_id: int) -> bool:
        pass

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> list[int]:
        pass

    @abstractmethod
    async def get_user_group(self, user_group: UserGroup) -> UserGroup | None:
        pass
