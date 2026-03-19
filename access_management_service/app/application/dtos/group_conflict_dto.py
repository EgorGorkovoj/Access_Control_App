from dataclasses import dataclass


@dataclass
class GroupConflictDTO:
    group_id: int
    conflict_group_id: int
