from abc import ABC, abstractmethod
from typing import Sequence

from app.domain.models.access import Access


class IAccessRepository(ABC):
    @abstractmethod
    async def get_by_id(self, access_id: int) -> Access | None:
        pass

    @abstractmethod
    async def get_all(self) -> Sequence[Access]:
        pass

    @abstractmethod
    async def create(self, access: Access) -> Access:
        pass

    @abstractmethod
    async def get_accesses_for_resource(self, resource_id: int) -> Sequence[Access]:
        pass
