from dataclasses import dataclass


@dataclass(frozen=True)
class GroupConflict:
    group_id: int
    conflict_group_id: int
