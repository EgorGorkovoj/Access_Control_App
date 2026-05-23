from pydantic import BaseModel, ConfigDict, field_validator

from app.application.dtos.access_request_dto import CreateAccessRequestDTO
from app.domain.models.access_request import RequestStatus, TargetType


class AccessRequestCreate(BaseModel):
    request_id: str
    user_id: int
    target_type: TargetType
    target_id: int
    # access_id: int | None = None
    # group_id: int | None = None

    @field_validator('target_id', mode='before')
    def normalize_zero(cls, value):
        return None if value == 0 else value

    def to_dto(self) -> CreateAccessRequestDTO:
        return CreateAccessRequestDTO(
            request_id=self.request_id,
            user_id=self.user_id,
            target_type=self.target_type,
            target_id=self.target_id,
        )


class UpdateRequestStatusRequest(BaseModel):
    status: RequestStatus
    changed_by: int | None = None


class RevokeUserPermissionRequest(BaseModel):
    target_type: TargetType
    target_id: int


class AccessRequestResponse(BaseModel):
    request_id: str
    user_id: int
    access_id: int | None = None
    group_id: int | None = None
    current_status: str

    model_config = ConfigDict(
        exclude_none=True,
        from_attributes=True,
    )

    @classmethod
    def from_dto(cls, obj):
        return cls(
            request_id=obj.request_id,
            user_id=obj.user_id,
            access_id=obj.access_id,
            group_id=obj.group_id,
            current_status=obj.current_status,
        )
