from dataclasses import dataclass


@dataclass(frozen=True)
class UserGroup:
    user_id: int
    group_id: int
