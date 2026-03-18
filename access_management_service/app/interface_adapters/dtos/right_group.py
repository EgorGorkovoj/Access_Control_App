from pydantic import BaseModel

from app.application.dtos.group_dto import CreateRightGroupDTO, RightGroupDTO, UpdateRightGroupDTO


class RightGroupCreate(BaseModel):
    name: str
    description: str | None = None

    def to_dto(self) -> CreateRightGroupDTO:
        return CreateRightGroupDTO(name=self.name, description=self.description)


class RightGroupUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    def to_dto(self, group_id: int) -> UpdateRightGroupDTO:
        return UpdateRightGroupDTO(
            id=group_id,
            name=self.name,
            description=self.description,
        )


class RightGroupResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    @classmethod
    def from_dto(cls, dto: RightGroupDTO) -> 'RightGroupResponse':
        return cls(id=dto.id, name=dto.name, description=dto.description)
