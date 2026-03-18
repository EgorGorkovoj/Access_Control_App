from dataclasses import dataclass
from enum import StrEnum
from typing import Optional


class RequestStatus(StrEnum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    APPROVED = 'approved'
    REJECTED = 'rejected'


@dataclass
class AccessRequest:
    request_id: str
    user_id: int
    access_id: Optional[int] = None
    group_id: Optional[int] = None
    current_status: RequestStatus = RequestStatus.PENDING
