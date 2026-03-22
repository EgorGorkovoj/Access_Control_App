from app.application.dtos.resource_dto import CreateResourceDTO, ResourceDTO, UpdateResourceDTO
from app.application.exceptions.resource import ResourceAlreadyExistsError, ResourceNotExistsError
from app.domain.models.resource import Resource
from app.domain.repositories.resource_repository import IResourceRepository


class ResourceService:
    def __init__(self, resource_repo: IResourceRepository):
        self.resource_repo = resource_repo

    async def create_resource(self, dto: CreateResourceDTO) -> ResourceDTO:
        existing = await self.resource_repo.get_by_name_and_type(dto.name, dto.type)
        if existing:
            raise ResourceAlreadyExistsError(dto.name, dto.type)

        resource = Resource(name=dto.name, type=dto.type, attributes=dto.attributes)

        created = await self.resource_repo.create(resource)

        return ResourceDTO(
            id=created.id, name=created.name, type=created.type, attributes=created.attributes
        )

    async def get_all_resources(self, limit: int | None, offset: int) -> list[ResourceDTO]:
        resources = await self.resource_repo.get_all(limit, offset)
        return [
            ResourceDTO(
                id=resource.id,
                name=resource.name,
                type=resource.type,
                attributes=resource.attributes,
            )
            for resource in resources
        ]

    async def get_resource(self, resource_id: int) -> ResourceDTO:
        resource = await self.resource_repo.get_by_id(resource_id)
        if resource is None:
            raise ResourceNotExistsError(resource_id)
        return ResourceDTO(
            id=resource.id, name=resource.name, type=resource.type, attributes=resource.attributes
        )

    async def update_resource(self, dto_update: UpdateResourceDTO) -> ResourceDTO:
        domain_model = Resource(
            id=dto_update.id,
            name=dto_update.name,
            type=dto_update.type,
            attributes=dto_update.attributes,
        )
        updated = await self.resource_repo.update(domain_model)

        if updated is None:
            raise ResourceNotExistsError(dto_update.id)

        return ResourceDTO(
            id=updated.id, name=updated.name, type=updated.type, attributes=updated.attributes
        )

    async def delete_resource(self, resource_id: int) -> None:
        deleted = await self.resource_repo.delete(resource_id)
        if not deleted:
            raise ResourceNotExistsError(resource_id)
