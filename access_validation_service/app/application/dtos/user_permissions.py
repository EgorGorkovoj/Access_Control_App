from dataclasses import dataclass


@dataclass
class UserPermissionsDTO:
    user_id: int
    user_groups: list[int] | None = None
    conflicting_groups: list[int] | None = None
    conflicting_accesses: list[int] | None = None
