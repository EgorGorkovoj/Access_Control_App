from abc import ABC, abstractmethod

from app.domain.models.request_status import RequestStatus


class IRequestStatusUpdater(ABC):
    @abstractmethod
    async def update_status(self, request_id: str, status: RequestStatus) -> None:
        pass
