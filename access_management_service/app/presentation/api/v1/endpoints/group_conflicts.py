from fastapi import APIRouter, Depends, status

from app.application.services.group_conflict_service import GroupConflictService
from app.interface_adapters.dtos.group_conflict import (
    GroupConflictResponse,
    GroupConflictsIDSResponse,
)
from app.presentation.dependencies import get_group_conflict_service_impl

router = APIRouter()


@router.post(
    '/groups/{group_id}/conflicts/{conflicting_group_id}', status_code=status.HTTP_201_CREATED
)
async def add_group_conflict(
    group_id: int,
    conflicting_group_id: int,
    group_conflict_service: GroupConflictService = Depends(get_group_conflict_service_impl),
) -> GroupConflictResponse:
    """Добавляет конфликт между двумя группами."""
    dto = await group_conflict_service.add_group_conflict(group_id, conflicting_group_id)
    return GroupConflictResponse.from_dto(dto)


@router.delete(
    '/groups/{group_id}/conflicts/{conflicting_group_id}', status_code=status.HTTP_204_NO_CONTENT
)
async def remove_group_conflict(
    group_id: int,
    conflicting_group_id: int,
    group_conflict_service: GroupConflictService = Depends(get_group_conflict_service_impl),
) -> None:
    """Удаляет конфликт групп."""
    await group_conflict_service.remove_group_conflict(group_id, conflicting_group_id)


# @router.get('/groups/{group_id}/conflicts', status_code=status.HTTP_200_OK)
# async def get_group_conflicts(
#     group_id: int,
#     group_conflict_service: GroupConflictService = Depends(get_group_conflict_service_impl),
# ) -> list[GroupConflictResponse]:
#     """Возвращает список конфликтующих групп для определенной группы."""
#     conflicts = await group_conflict_service.get_group_conflicts(group_id)
#     return [GroupConflictResponse.from_dto(dto) for dto in conflicts]


@router.get('/groups/{group_id}/conflicts', status_code=status.HTTP_200_OK)
async def get_group_conflicts_ids(
    group_id: int,
    group_conflict_service: GroupConflictService = Depends(get_group_conflict_service_impl),
) -> GroupConflictsIDSResponse:
    """Возвращает список конфликтующих групп для определенной группы."""
    conflicts = await group_conflict_service.get_conflicting_group_ids(group_id)
    return GroupConflictsIDSResponse(group_id=group_id, conflicting_group_ids=conflicts)
