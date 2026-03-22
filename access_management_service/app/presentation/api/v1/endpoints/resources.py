from fastapi import APIRouter, Depends, Query, status

from app.application.services.resource_service import ResourceService
from app.interface_adapters.dtos.resource import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)
from app.presentation.dependencies import get_resource_service

router = APIRouter()


@router.post('/resources', status_code=status.HTTP_201_CREATED)
async def create_resource(
    data_resources: ResourceCreate,
    resource_service: ResourceService = Depends(get_resource_service),
) -> ResourceResponse:
    dto_resource = data_resources.to_dto()
    created_resource = await resource_service.create_resource(dto_resource)
    return ResourceResponse.from_dto(created_resource)


@router.get('/resources', status_code=status.HTTP_200_OK)
async def get_resources(
    limit: int | None = Query(None, ge=1, le=100),
    offset: int = Query(0, ge=0),
    resource_service: ResourceService = Depends(get_resource_service),
) -> list[ResourceResponse]:
    """Возвращает список всех ресурсов."""
    resources = await resource_service.get_all_resources(limit, offset)
    return [ResourceResponse.from_dto(resource) for resource in resources]


@router.get('/resources/{resource_id}', status_code=status.HTTP_200_OK)
async def get_resource(
    resource_id: int,
    resource_service: ResourceService = Depends(get_resource_service),
) -> ResourceResponse:
    """Возвращает один ресурс по id."""
    resource = await resource_service.get_resource(resource_id)
    return ResourceResponse.from_dto(resource)


@router.patch('/resources/{resource_id}', status_code=status.HTTP_200_OK)
async def update_resource(
    resource_id: int,
    data_update_resource: ResourceUpdate,
    resource_service: ResourceService = Depends(get_resource_service),
) -> ResourceResponse:
    """Обновляет ресурс."""
    update_dto_resource = data_update_resource.to_dto(resource_id)
    updating_resource = await resource_service.update_resource(update_dto_resource)
    return ResourceResponse.from_dto(updating_resource)


@router.delete('/resources/{resource_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: int, resource_service: ResourceService = Depends(get_resource_service)
) -> None:
    """Удаляет ресур."""
    await resource_service.delete_resource(resource_id)
