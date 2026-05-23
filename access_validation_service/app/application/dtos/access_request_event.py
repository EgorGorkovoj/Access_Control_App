from dataclasses import dataclass
from enum import StrEnum


class TargetType(StrEnum):
    ACCESS = 'access'
    GROUP = 'group'


@dataclass
class ValidationRequestDTO:
    request_id: str
    user_id: int
    target_type: TargetType
    target_id: int


# class AccessRequestEvent(BaseModel):
#     request_id: str
#     user_id: int
#     group_id: int
