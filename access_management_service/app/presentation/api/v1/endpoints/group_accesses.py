from fastapi import APIRouter, Depends, status

from app.application.services.group_access_service import GroupAccessService
from app.interface_adapters.dtos.group_access import GroupAccessResponse
from app.presentation.dependencies import get_group_access_service

router = APIRouter()


@router.post('/groups/{group_id}/accesses/{access_id}', status_code=status.HTTP_201_CREATED)
async def add_access_to_group(
    group_id: int, access_id: int, service: GroupAccessService = Depends(get_group_access_service)
) -> GroupAccessResponse:
    """Назначает access группе."""
    group_access_dto = await service.add_access_to_group(group_id, access_id)
    return GroupAccessResponse.from_dto(group_access_dto)


@router.delete('/groups/{group_id}/accesses/{access_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_permission_from_group(
    group_id: int, access_id: int, service: GroupAccessService = Depends(get_group_access_service)
) -> None:
    """Удаляет access у группы."""
    await service.remove_access_from_group(group_id, access_id)


@router.get('/groups/{group_id}/accesses', status_code=status.HTTP_200_OK)
async def get_group_accesses(
    group_id: int, service: GroupAccessService = Depends(get_group_access_service)
) -> list[GroupAccessResponse]:
    """Возвращает список accesses группы."""
    group_accesses_dto = await service.get_group_accesses(group_id)
    return [GroupAccessResponse.from_dto(group_access) for group_access in group_accesses_dto]
