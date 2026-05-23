from app.application.dtos.access_request_event import (
    TargetType,
    ValidationRequestDTO,
)
from app.application.services.validation_service import ValidationService


class AccessRequestHandler:
    def __init__(self, validation_service: ValidationService):
        self.validation_service = validation_service

    async def handle(self, event: dict):
        dto = ValidationRequestDTO(
            request_id=event['request_id'],
            user_id=event['user_id'],
            target_type=TargetType(event['target_type']),
            target_id=event['target_id'],
        )

        await self.validation_service.validate_request(dto)
