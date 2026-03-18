from abc import ABC, abstractmethod
from typing import Sequence

from app.domain.models.resource import Resource


class IResourceRepository(ABC):
    @abstractmethod
    async def get_by_id(self, resource_id: int) -> Resource | None:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Resource | None:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Resource]:
        pass

    @abstractmethod
    async def create(self, resource: Resource) -> Resource:
        pass
