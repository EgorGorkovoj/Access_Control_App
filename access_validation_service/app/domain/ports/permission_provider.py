from abc import ABC, abstractmethod

from app.application.dtos.access_request_event import TargetType
from app.application.dtos.user_permissions import UserPermissionsDTO


class IUserPermissionProvider(ABC):
    @abstractmethod
    async def get_user_permissions(
        self,
        user_id: int,
        target_type: TargetType,
        target_id: int,
    ) -> UserPermissionsDTO:
        pass
