from dataclasses import dataclass


@dataclass(frozen=True)
class UserAccessDTO:
    user_id: int
    access_id: int
