from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.application.dtos.access_request_dto import (
    AccessRequestDTO,
    AccessRequestWithHistoryDTO,
    CreateAccessRequestDTO,
)
from app.domain.models.access_request import RequestStatus, TargetType


class RequestBase(BaseModel):
    request_id: str
    user_id: int


class AccessRequestBase(RequestBase):
    access_id: int | None = None
    group_id: int | None = None


class AccessRequestCreate(RequestBase):
    target_type: TargetType
    target_id: int

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


class AccessRequestResponse(AccessRequestBase):
    current_status: str

    model_config = ConfigDict(
        exclude_none=True,
        from_attributes=True,
    )

    @classmethod
    def from_dto(cls, obj: AccessRequestDTO) -> 'AccessRequestResponse':
        return cls(
            request_id=obj.request_id,
            user_id=obj.user_id,
            access_id=obj.access_id,
            group_id=obj.group_id,
            current_status=obj.current_status,
        )


class AccessRequestStatusHistoryResponse(BaseModel):
    status: RequestStatus
    changed_at: datetime
    changed_by: int | None = None


class AccessRequestWithHistoryResponse(AccessRequestBase):
    current_status: str
    status_history: list[AccessRequestStatusHistoryResponse] = Field(default_factory=list)

    @classmethod
    def from_dto(cls, dto: AccessRequestWithHistoryDTO) -> 'AccessRequestWithHistoryResponse':
        return cls(
            request_id=dto.request_id,
            user_id=dto.user_id,
            access_id=dto.access_id,
            group_id=dto.group_id,
            current_status=dto.current_status,
            status_history=[
                AccessRequestStatusHistoryResponse(
                    status=history.status,
                    changed_at=history.changed_at,
                    changed_by=history.changed_by,
                )
                for history in (dto.status_history or [])
            ],
        )
