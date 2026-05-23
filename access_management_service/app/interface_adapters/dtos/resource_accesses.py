from typing import Any

from pydantic import BaseModel

from app.application.dtos.resource_access_dto import AccessCredentialsDTO, ResourceAccessesDTO


class AccessCredentialsResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    credentials: dict[str, Any]

    @classmethod
    def from_dto(cls, dto: AccessCredentialsDTO):
        return cls(
            id=dto.id, name=dto.name, description=dto.description, credentials=dto.credentials
        )


class ResourceAccessesResponse(BaseModel):
    resource_id: int
    resource_name: str
    resource_type: str
    accesses: list[AccessCredentialsResponse]

    @classmethod
    def from_dto(cls, dto: ResourceAccessesDTO) -> 'ResourceAccessesResponse':
        return cls(
            resource_id=dto.resource_id,
            resource_name=dto.resource_name,
            resource_type=dto.resource_type,
            accesses=[AccessCredentialsResponse.from_dto(access) for access in dto.accesses],
        )
