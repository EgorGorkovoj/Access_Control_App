from dataclasses import dataclass


@dataclass
class UserPermissionsDTO:
    user_id: int
    user_accesses: list[int]
    user_groups: list[int] | None = None
    accesses_destination_group: list[int] | None = None
    conflicting_groups: list[int] | None = None
