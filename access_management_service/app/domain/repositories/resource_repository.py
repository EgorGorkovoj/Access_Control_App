from abc import ABC, abstractmethod
from typing import Sequence

from app.domain.models.resource import Resource


class IResourceRepository(ABC):
    @abstractmethod
    async def get_by_id(self, resource_id: int) -> Resource | None:
        pass

    @abstractmethod
    async def get_all(self, limit: int | None, offset: int) -> Sequence[Resource]:
        pass

    @abstractmethod
    async def get_by_name_and_type(self, name: str, type: str) -> Resource | None:
        pass

    @abstractmethod
    async def create(self, resource: Resource) -> Resource:
        pass

    @abstractmethod
    async def update(self, resource: Resource) -> Resource | None:
        pass

    @abstractmethod
    async def delete(self, resource_id: int) -> bool:
        pass
