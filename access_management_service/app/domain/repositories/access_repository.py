from abc import ABC, abstractmethod
from typing import Sequence

from app.domain.models.access import Access, AccessCreate


class IAccessRepository(ABC):
    @abstractmethod
    async def create(self, access: AccessCreate) -> Access:
        pass

    @abstractmethod
    async def get_all(self, limit: int | None, offset: int) -> Sequence[Access]:
        pass

    @abstractmethod
    async def get_by_id(self, access_id: int) -> Access | None:
        pass

    @abstractmethod
    async def get_by_resource_id(self, resource_id: int) -> list[Access]:
        pass

    @abstractmethod
    async def get_by_name_and_resource(self, name: str, resource_id: int) -> Access | None:
        pass

    @abstractmethod
    async def delete(self, access_id: int) -> bool:
        pass
