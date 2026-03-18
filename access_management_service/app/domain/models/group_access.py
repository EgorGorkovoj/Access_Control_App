from dataclasses import dataclass


@dataclass(frozen=True)
class GroupAccess:
    group_id: int
    access_id: int
