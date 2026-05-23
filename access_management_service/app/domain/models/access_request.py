from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class TargetType(StrEnum):
    GROUP = 'group'
    ACCESS = 'access'


class RequestStatus(StrEnum):
    PENDING = 'pending'
    IN_PROGRESS = 'in progress'
    APPROVED = 'approved'
    REJECTED = 'rejected'


@dataclass(frozen=True)
class AccessRequestStatusHistory:
    status: RequestStatus
    changed_at: datetime
    changed_by: int | None


@dataclass
class AccessRequest:
    request_id: str
    user_id: int
    access_id: int | None = None
    group_id: int | None = None
    current_status: RequestStatus = RequestStatus.PENDING
    id: int | None = None

    status_history: list[AccessRequestStatusHistory] | None = None
