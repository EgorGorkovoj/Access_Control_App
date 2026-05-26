from abc import ABC, abstractmethod

from app.application.dtos.access_request_event import TargetType


class IPermissionGrantProvider(ABC):
    @abstractmethod
    async def grant(self, user_id: int, target_type: TargetType, target_id: int) -> None:
        pass
