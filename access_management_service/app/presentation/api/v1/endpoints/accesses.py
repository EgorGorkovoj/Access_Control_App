from fastapi import APIRouter, Depends, Query, status

from app.application.services.access_service import AccessService
from app.interface_adapters.dtos.access import AccessCreate, AccessResponse
from app.presentation.dependencies import get_access_service

router = APIRouter()


@router.post('/accesses', status_code=status.HTTP_201_CREATED)
async def create_access(
    data_access: AccessCreate, access_service: AccessService = Depends(get_access_service)
) -> AccessResponse:
    access_dto = data_access.to_dto()
    access = await access_service.create_access(access_dto)
    return AccessResponse.from_dto(access)


@router.get('/accesses', status_code=status.HTTP_200_OK)
async def get_accesses(
    limit: int | None = Query(None, ge=1, le=100),
    offset: int = Query(0, ge=0),
    access_service: AccessService = Depends(get_access_service),
) -> list[AccessResponse]:
    accesses = await access_service.get_accesses(limit, offset)
    return [AccessResponse.from_dto(access) for access in accesses]


@router.get('/accesses/{access_id}', status_code=status.HTTP_200_OK)
async def get_access(
    access_id: int, access_service: AccessService = Depends(get_access_service)
) -> AccessResponse:
    access = await access_service.get_access(access_id)
    return AccessResponse.from_dto(access)


@router.delete('/accesses/{access_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_access(
    access_id: int, access_service: AccessService = Depends(get_access_service)
) -> None:
    await access_service.delete_access(access_id)
