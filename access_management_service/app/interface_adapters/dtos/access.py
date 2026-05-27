from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.application.dtos.access_dto import AccessDTO, CreateAccessDTO


class AccessCreate(BaseModel):
    name: str
    description: str | None = None
    resource_id: int = Field(..., gt=0)
    credentials: dict[str, Any] = Field(default_factory=dict)

    def to_dto(self) -> CreateAccessDTO:
        return CreateAccessDTO(
            name=self.name,
            description=self.description,
            resource_id=self.resource_id,
            credentials=self.credentials,
        )

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'name': 'FullAccess-Main-Prod',
                'description': 'Полный доступ к продакшен БД',
                'resource_id': 5,
                'credentials': {
                    'host': 'db.prod.company.ru',
                    'port': 5432,
                    'username': 'company_user',
                },
            }
        }
    )


class AccessResponse(BaseModel):
    id: int
    name: str
    description: str | None
    resource_id: int
    credentials: dict[str, Any]
    is_active: bool

    @classmethod
    def from_dto(cls, dto: AccessDTO) -> 'AccessResponse':
        return cls(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            resource_id=dto.resource_id,
            credentials=dto.credentials,
            is_active=dto.is_active,
        )
