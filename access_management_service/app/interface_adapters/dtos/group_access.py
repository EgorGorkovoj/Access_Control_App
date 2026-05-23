from pydantic import BaseModel, ConfigDict

from app.application.dtos.group_access_dto import GroupAccessDTO


class GroupAccessIdsResponse(BaseModel):
    """Список ID доступов пользователя для определенной группы."""

    access_ids: list[int]

    model_config = ConfigDict(from_attributes=True)


class GroupAccessResponse(BaseModel):
    group_id: int
    access_id: int

    @classmethod
    def from_dto(cls, dto: GroupAccessDTO):
        return cls(group_id=dto.group_id, access_id=dto.access_id)
