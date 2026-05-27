from app.application.dtos.resource_access_dto import AccessCredentialsDTO, ResourceAccessesDTO
from app.application.exceptions.resource import ResourceNotExistsError
from app.domain.repositories.access_repository import IAccessRepository
from app.domain.repositories.resource_repository import IResourceRepository


class ResourceAccessService:
    def __init__(self, resource_repo: IResourceRepository, access_repo: IAccessRepository):
        self.resource_repo = resource_repo
        self.access_repo = access_repo

    async def get_accesses_by_resource(self, resource_id: int) -> ResourceAccessesDTO:
        resource = await self.resource_repo.get_by_id(resource_id)
        if resource is None:
            raise ResourceNotExistsError(resource_id=resource_id)

        accesses = await self.access_repo.get_by_resource_id(resource_id)

        access_dtos = [
            AccessCredentialsDTO(
                id=access.id,
                name=access.name,
                description=access.description,
                credentials=access.credentials,
            )
            for access in accesses
        ]

        return ResourceAccessesDTO(
            resource_id=resource.id,
            resource_name=resource.name,
            resource_type=resource.type,
            accesses=access_dtos,
        )
