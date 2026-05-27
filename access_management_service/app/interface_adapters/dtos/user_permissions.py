from pydantic import BaseModel, ConfigDict

from app.application.dtos.user_permissions_dto import UserPermissionQueryDTO, UserPermissionsDTO
from app.domain.models.access_request import TargetType


class UserPermissionsRequest(BaseModel):
    user_id: int
    target_type: TargetType
    target_id: int


class UserPermissionsResponse(BaseModel):
    user_id: int
    user_groups: list[int] | None = None
    conflicting_groups: list[int] | None = None
    conflicting_accesses: list[int] | None = None

    model_config = ConfigDict(from_attributes=True, exclude_none=True)

    @classmethod
    def from_dto(cls, dto: UserPermissionsDTO) -> 'UserPermissionsResponse':
        return cls(
            user_id=dto.user_id,
            user_groups=dto.user_groups,
            conflicting_groups=dto.conflicting_groups,
            conflicting_accesses=dto.conflicting_accesses,
        )


class UserAccessPermissionsResponse(BaseModel):
    access_ids: list[int]

    @classmethod
    def from_dto(cls, dto: UserPermissionQueryDTO) -> 'UserAccessPermissionsResponse':
        return cls(
            access_ids=dto.access_ids,
        )
