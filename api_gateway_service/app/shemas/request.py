from typing import Literal

from pydantic import BaseModel, Field


class CreateAccessRequestSchema(BaseModel):
    user_id: int
    target_type: Literal['group', 'access']
    target_id: int
    # group_id: int


class AccessRequestResponseSchema(BaseModel):
    request_id: str
    status: str = Field(default='pending')
    message: str = Field(default='Request accepted for processing')
