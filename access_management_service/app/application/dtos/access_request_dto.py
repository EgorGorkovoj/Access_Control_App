from dataclasses import dataclass
from datetime import datetime

from app.domain.models.access_request import RequestStatus, TargetType


@dataclass
class CreateAccessRequestDTO:
    request_id: str
    user_id: int
    target_type: TargetType
    target_id: int


@dataclass
class AccessRequestDTO:
    request_id: str
    user_id: int
    access_id: int | None
    group_id: int | None
    current_status: RequestStatus


@dataclass
class AccessRequestStatusHistoryDTO:
    status: RequestStatus
    changed_at: datetime
    changed_by: int | None


@dataclass
class AccessRequestWithHistoryDTO:
    request_id: str
    user_id: int
    access_id: int | None
    group_id: int | None
    current_status: RequestStatus
    status_history: list[AccessRequestStatusHistoryDTO]
