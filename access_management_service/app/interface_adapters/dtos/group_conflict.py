from pydantic import BaseModel, ConfigDict

from app.application.dtos.group_conflict_dto import GroupConflictDTO


class GroupConflictsIDSResponse(BaseModel):
    """Ответ с ID конфликтующих групп"""

    group_id: int
    conflicting_group_ids: list[int]

    model_config = ConfigDict(from_attributes=True)


class GroupConflictResponse(BaseModel):
    group_id: int
    conflict_group_id: int

    @classmethod
    def from_dto(cls, dto: GroupConflictDTO) -> 'GroupConflictResponse':
        return cls(
            group_id=dto.group_id,
            conflict_group_id=dto.conflict_group_id,
        )
