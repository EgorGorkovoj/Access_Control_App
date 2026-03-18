from fastapi import APIRouter, Depends, Query, status

from app.application.services.right_group_service import RightGroupService
from app.interface_adapters.dtos.right_group import (
    RightGroupCreate,
    RightGroupResponse,
    RightGroupUpdate,
)
from app.presentation.dependencies import get_right_group_service

router = APIRouter()


@router.post('/right-group', status_code=status.HTTP_201_CREATED)
async def create_right_group(
    data_group: RightGroupCreate,
    right_group_service: RightGroupService = Depends(get_right_group_service),
) -> RightGroupResponse:
    dto_group = data_group.to_dto()
    created_group = await right_group_service.create_right_group(dto_group)
    return RightGroupResponse.from_dto(created_group)


@router.get('/right-groups', status_code=status.HTTP_200_OK)
async def get_right_groups(
    limit: int | None = Query(None, ge=1, le=100),
    offset: int = Query(0, ge=0),
    right_group_service: RightGroupService = Depends(get_right_group_service),
) -> list[RightGroupResponse]:
    """Возвращает список всех групп прав."""
    groups = await right_group_service.get_right_groups(limit=limit, offset=offset)
    return [RightGroupResponse.from_dto(group) for group in groups]


@router.get('/right-groups/{group_id}', status_code=status.HTTP_200_OK)
async def get_right_group(
    group_id: int, right_group_service: RightGroupService = Depends(get_right_group_service)
):
    """Возвращает одну группу прав по id."""
    group = await right_group_service.get_right_group(group_id=group_id)
    return RightGroupResponse.from_dto(group)


@router.patch('/right-groups/{group_id}', status_code=status.HTTP_200_OK)
async def update_right_group(
    group_id: int,
    data_update_group: RightGroupUpdate,
    right_group_service: RightGroupService = Depends(get_right_group_service),
) -> RightGroupResponse:
    """Обновляет имя или описание группы."""
    update_dto_group = data_update_group.to_dto(group_id)
    updating_group = await right_group_service.update_right_group(update_dto_group)
    return RightGroupResponse.from_dto(updating_group)


@router.delete('/right-groups/{group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_right_group(
    group_id: int, right_group_service: RightGroupService = Depends(get_right_group_service)
) -> None:
    """Удаляет группу прав."""
    await right_group_service.delete_right_group(group_id)
