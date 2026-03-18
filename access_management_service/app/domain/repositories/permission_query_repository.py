from abc import ABC, abstractmethod
from typing import Sequence

from app.domain.models.access import Access


class IPermissionQueryRepository(ABC):
    @abstractmethod
    async def get_user_accesses(self, user_id: int) -> Sequence[Access]:
        pass
