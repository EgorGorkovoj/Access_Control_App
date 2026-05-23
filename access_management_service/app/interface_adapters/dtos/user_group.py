from pydantic import BaseModel, ConfigDict

from app.application.dtos.user_group_dto import UserGroupDTO


class UserGroupIdsResponse(BaseModel):
    """Список ID групп пользователя"""

    group_ids: list[int]

    model_config = ConfigDict(from_attributes=True)


class UserGroupResponse(BaseModel):
    user_id: int
    group_id: int

    @classmethod
    def from_dto(cls, dto: UserGroupDTO):
        return cls(user_id=dto.user_id, group_id=dto.group_id)
