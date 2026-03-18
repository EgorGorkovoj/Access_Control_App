from abc import ABC, abstractmethod
from typing import Sequence


class IUserAccessRepository(ABC):
    @abstractmethod
    async def add_group(self, user_id: int, group_id: int) -> None:
        pass

    @abstractmethod
    async def remove_group(self, user_id: int, group_id: int) -> None:
        pass

    @abstractmethod
    async def add_access(self, user_id: int, access_id: int) -> None:
        pass

    @abstractmethod
    async def remove_access(self, user_id: int, access_id: int) -> None:
        pass

    @abstractmethod
    async def get_user_groups(self, user_id: int) -> Sequence[int]:
        pass

    @abstractmethod
    async def get_user_direct_access(self, user_id: int) -> Sequence[int]:
        """Доступы выданные напрямую без добавления в группу."""
        pass
