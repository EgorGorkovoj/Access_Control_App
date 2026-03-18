from dataclasses import dataclass


@dataclass(frozen=True)
class UserAccess:
    user_id: int
    access_id: int
