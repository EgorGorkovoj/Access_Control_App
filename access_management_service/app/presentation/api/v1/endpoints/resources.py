from fastapi import APIRouter, Depends, Query, status

from app.application.services.resource_access_service import ResourceAccessService
from app.application.services.resource_service import ResourceService
from app.interface_adapters.dtos.resource import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)
from app.interface_adapters.dtos.resource_accesses import ResourceAccessesResponse
from app.presentation.dependencies import get_resource_access_service, get_resource_service

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
    resources = await resource_service.get_all_resources(limit, offset)
    return [ResourceResponse.from_dto(resource) for resource in resources]


@router.get('/resources/{resource_id}', status_code=status.HTTP_200_OK)
async def get_resource(
    resource_id: int,
    resource_service: ResourceService = Depends(get_resource_service),
) -> ResourceResponse:
    resource = await resource_service.get_resource(resource_id)
    return ResourceResponse.from_dto(resource)


@router.get(
    '/resources/{resource_id}/accesses',
    status_code=status.HTTP_200_OK,
    response_model=ResourceAccessesResponse,
)
async def get_resource_accesses(
    resource_id: int, service: ResourceAccessService = Depends(get_resource_access_service)
) -> ResourceAccessesResponse:
    dto = await service.get_accesses_by_resource(resource_id)
    return ResourceAccessesResponse.from_dto(dto)


@router.patch('/resources/{resource_id}', status_code=status.HTTP_200_OK)
async def update_resource(
    resource_id: int,
    data_update_resource: ResourceUpdate,
    resource_service: ResourceService = Depends(get_resource_service),
) -> ResourceResponse:
    update_dto_resource = data_update_resource.to_dto(resource_id)
    updating_resource = await resource_service.update_resource(update_dto_resource)
    return ResourceResponse.from_dto(updating_resource)


@router.delete('/resources/{resource_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: int, resource_service: ResourceService = Depends(get_resource_service)
) -> None:
    await resource_service.delete_resource(resource_id)
