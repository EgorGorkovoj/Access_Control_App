from fastapi import APIRouter, Depends, status

from app.application.services.access_request_service import AccessRequestService
from app.interface_adapters.dtos.request import (
    AccessRequestCreate,
    AccessRequestResponse,
    UpdateRequestStatusRequest,
)
from app.presentation.dependencies import get_request_service

router = APIRouter()


@router.post(
    '/request',
    status_code=status.HTTP_201_CREATED,
    response_model=AccessRequestResponse,
    response_model_exclude_none=True,
)
async def create_access_request(
    data: AccessRequestCreate,
    service: AccessRequestService = Depends(get_request_service),
) -> AccessRequestResponse:
    dto = data.to_dto()
    created = await service.create_request(dto)
    return AccessRequestResponse.from_dto(created)


@router.patch('/request/{request_id}/update-status', status_code=status.HTTP_200_OK)
async def update_access_request_status(
    request_id: str,
    update_data: UpdateRequestStatusRequest,
    service: AccessRequestService = Depends(get_request_service),
):
    await service.update_status(
        request_id=request_id,
        status=update_data.status,
        changed_by=update_data.changed_by,
    )
