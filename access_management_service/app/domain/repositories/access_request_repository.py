from abc import ABC, abstractmethod

from app.domain.models.access_request import AccessRequest, RequestStatus


class IAccessRequestRepository(ABC):
    @abstractmethod
    async def create(self, group_access: AccessRequest) -> AccessRequest:
        pass

    @abstractmethod
    async def get_by_request_id(self, request_id: str) -> AccessRequest | None:
        pass

    @abstractmethod
    async def get_with_history(self, request_id: str) -> AccessRequest | None:
        pass

    @abstractmethod
    async def change_status(
        self,
        request_id: str,
        status: RequestStatus,
        changed_by: int | None = None,
    ) -> None:
        pass
