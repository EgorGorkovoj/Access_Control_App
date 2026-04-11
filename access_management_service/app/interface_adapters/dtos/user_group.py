from pydantic import BaseModel

from app.application.dtos.user_group_dto import UserGroupDTO


class UserGroupResponse(BaseModel):
    user_id: int
    group_id: int

    @classmethod
    def from_dto(cls, dto: UserGroupDTO):
        return cls(user_id=dto.user_id, group_id=dto.group_id)
