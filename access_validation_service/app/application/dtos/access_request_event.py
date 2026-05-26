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
