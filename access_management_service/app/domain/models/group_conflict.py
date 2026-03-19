from dataclasses import dataclass


@dataclass(frozen=True)
class GroupConflict:
    group_id: int
    conflict_group_id: int

    def normalized(self) -> tuple[int, int]:
        return tuple(sorted((self.group_id, self.conflict_group_id)))
