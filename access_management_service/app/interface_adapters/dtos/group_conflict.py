from pydantic import BaseModel

from app.application.dtos.group_conflict_dto import GroupConflictDTO


class GroupConflictResponse(BaseModel):
    group_id: int
    conflict_group_id: int

    @classmethod
    def from_dto(cls, dto: GroupConflictDTO) -> 'GroupConflictResponse':
        return cls(
            group_id=dto.group_id,
            conflict_group_id=dto.conflict_group_id,
        )
