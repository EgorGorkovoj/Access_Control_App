from pydantic import BaseModel

from app.application.dtos.group_access_dto import GroupAccessDTO


class GroupAccessResponse(BaseModel):
    group_id: int
    access_id: int

    @classmethod
    def from_dto(cls, dto: GroupAccessDTO):
        return cls(group_id=dto.group_id, access_id=dto.access_id)
