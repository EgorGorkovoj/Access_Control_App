from pydantic import BaseModel

from app.domain.models.access_request import TargetType


class GrantPermissionsRequest(BaseModel):
    user_id: int
    target_type: TargetType
    target_id: int
