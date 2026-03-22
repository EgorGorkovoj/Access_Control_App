from pydantic import BaseModel

from app.application.dtos.access_dto import AccessDTO, CreateAccessDTO


class AccessCreate(BaseModel):
    name: str
    description: str | None = None
    resource_id: int

    def to_dto(self) -> CreateAccessDTO:
        return CreateAccessDTO(
            name=self.name, description=self.description, resource_id=self.resource_id
        )


class AccessResponse(BaseModel):
    id: int
    name: str
    description: str | None
    resource_id: int

    @classmethod
    def from_dto(cls, dto: AccessDTO):
        return cls(
            id=dto.id, name=dto.name, description=dto.description, resource_id=dto.resource_id
        )
