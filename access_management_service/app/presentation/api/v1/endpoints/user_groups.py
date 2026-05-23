from fastapi import APIRouter, Depends, status

from app.application.services.user_group_service import UserGroupService
from app.interface_adapters.dtos.user_group import UserGroupIdsResponse, UserGroupResponse
from app.presentation.dependencies import get_user_group_service

router = APIRouter()


@router.post('/users/{user_id}/groups/{group_id}', status_code=status.HTTP_201_CREATED)
async def add_user_to_group(
    user_id: int, group_id: int, service: UserGroupService = Depends(get_user_group_service)
) -> UserGroupResponse:
    user_group = await service.add_user_to_group(user_id, group_id)
    return UserGroupResponse.from_dto(user_group)


@router.delete('/users/{user_id}/groups/{group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_from_group(
    user_id: int, group_id: int, service: UserGroupService = Depends(get_user_group_service)
) -> None:
    await service.remove_user_from_group(user_id, group_id)


@router.get('/users/{user_id}/groups', status_code=status.HTTP_200_OK)
async def get_user_groups(
    user_id: int, service: UserGroupService = Depends(get_user_group_service)
) -> UserGroupIdsResponse:
    group_ids = await service.get_user_groups_ids(user_id=user_id)
    return UserGroupIdsResponse(group_ids=group_ids)
