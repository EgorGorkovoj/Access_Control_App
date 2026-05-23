from abc import ABC, abstractmethod

from app.domain.models.user_access import UserAccess


class IUserAccessRepository(ABC):
    @abstractmethod
    async def add_access(self, user_access: UserAccess) -> UserAccess:
        pass

    @abstractmethod
    async def remove_access(self, user_id: int, access_id: int) -> bool:
        pass

    @abstractmethod
    async def get_all_user_accesses(self, user_id: int) -> list[int]:
        pass
