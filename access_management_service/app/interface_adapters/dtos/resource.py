from typing import Any

from pydantic import BaseModel

from app.application.dtos.resource_dto import CreateResourceDTO, ResourceDTO, UpdateResourceDTO


class ResourceCreate(BaseModel):
    name: str
    type: str
    attributes: dict[str, Any]

    def to_dto(self) -> CreateResourceDTO:
        return CreateResourceDTO(name=self.name, type=self.type, attributes=self.attributes)


class ResourceUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    attributes: dict[str, Any] | None = None
    is_active: bool | None = None

    def to_dto(self, resource_id: int) -> UpdateResourceDTO:
        return UpdateResourceDTO(
            id=resource_id,
            name=self.name,
            type=self.type,
            attributes=self.attributes,
            is_active=self.is_active,
        )


class ResourceResponse(BaseModel):
    id: int
    name: str
    type: str
    attributes: dict[str, Any]

    @classmethod
    def from_dto(cls, dto: ResourceDTO):
        return cls(id=dto.id, name=dto.name, type=dto.type, attributes=dto.attributes)
