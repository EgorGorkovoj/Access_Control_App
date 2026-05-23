from app.application.dtos.resource_dto import CreateResourceDTO, ResourceDTO, UpdateResourceDTO
from app.application.exceptions.resource import ResourceAlreadyExistsError, ResourceNotExistsError
from app.domain.models.resource import Resource, ResourceCreate
from app.domain.repositories.resource_repository import IResourceRepository


class ResourceService:
    def __init__(self, resource_repo: IResourceRepository):
        self.resource_repo = resource_repo

    async def create_resource(self, dto: CreateResourceDTO) -> ResourceDTO:
        existing = await self.resource_repo.get_by_name_and_type(dto.name, dto.type)
        if existing:
            raise ResourceAlreadyExistsError(dto.name, dto.type)

        resource = ResourceCreate(name=dto.name, type=dto.type, attributes=dto.attributes)

        created = await self.resource_repo.create(resource)

        return ResourceDTO(
            id=created.id,
            name=created.name,
            type=created.type,  # type: ignore
            attributes=created.attributes,
            is_active=created.is_active,
        )

    async def get_all_resources(self, limit: int | None, offset: int) -> list[ResourceDTO]:
        resources = await self.resource_repo.get_all(limit, offset)
        return [
            ResourceDTO(
                id=resource.id,
                name=resource.name,
                type=resource.type,
                attributes=resource.attributes,
                is_active=resource.is_active,
            )
            for resource in resources
        ]

    async def get_resource(self, resource_id: int) -> ResourceDTO:
        resource = await self.resource_repo.get_by_id(resource_id)
        if resource is None:
            raise ResourceNotExistsError(resource_id)
        return ResourceDTO(
            id=resource.id,
            name=resource.name,
            type=resource.type,  # type: ignore
            attributes=resource.attributes,
            is_active=resource.is_active,
        )

    async def update_resource(self, dto_update: UpdateResourceDTO) -> ResourceDTO:
        existing = await self.resource_repo.get_by_id(dto_update.id)

        if existing is None:
            raise ResourceNotExistsError(dto_update.id)

        domain_model = Resource(
            id=dto_update.id,
            name=(dto_update.name if dto_update.name is not None else existing.name),
            type=(dto_update.type if dto_update.type is not None else existing.type),
            attributes=(
                dto_update.attributes if dto_update.attributes is not None else existing.attributes
            ),
            is_active=(
                dto_update.is_active if dto_update.is_active is not None else existing.is_active
            ),
        )
        updated = await self.resource_repo.update(domain_model)

        return ResourceDTO(
            id=updated.id,
            name=updated.name,
            type=updated.type,  # type:ignore
            attributes=updated.attributes,
            is_active=updated.is_active,
        )

    async def delete_resource(self, resource_id: int) -> None:
        deleted = await self.resource_repo.delete(resource_id)
        if not deleted:
            raise ResourceNotExistsError(resource_id)
