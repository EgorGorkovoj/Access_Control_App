from app.application.dtos.access_dto import AccessDTO, CreateAccessDTO
from app.application.exceptions.access import AccessAlreadyExistsError, AccessNotFoundError
from app.application.exceptions.resource import ResourceNotExistsError
from app.domain.models.access import AccessCreate
from app.domain.repositories.access_repository import IAccessRepository
from app.domain.repositories.resource_repository import IResourceRepository


class AccessService:
    def __init__(self, access_repo: IAccessRepository, resource_repo: IResourceRepository):
        self.access_repo = access_repo
        self.resource_repo = resource_repo

    async def create_access(self, dto: CreateAccessDTO) -> AccessDTO:
        resource = await self.resource_repo.get_by_id(dto.resource_id)
        if not resource:
            raise ResourceNotExistsError(dto.resource_id)

        existing = await self.access_repo.get_by_name_and_resource(dto.name, dto.resource_id)

        if existing:
            raise AccessAlreadyExistsError(dto.name, dto.resource_id)

        access = AccessCreate(
            name=dto.name,
            description=dto.description,
            resource_id=dto.resource_id,
            credentials=dto.credentials,
            is_active=dto.is_active,
        )

        created = await self.access_repo.create(access)

        return AccessDTO(
            id=created.id,
            name=created.name,
            description=created.description,
            resource_id=created.resource_id,
            credentials=created.credentials,
            is_active=created.is_active,
        )

    async def get_accesses(self, limit: int | None, offset: int):
        accesses = await self.access_repo.get_all(limit, offset)

        return [
            AccessDTO(
                id=access.id,
                name=access.name,
                description=access.description,
                resource_id=access.resource_id,
                credentials=access.credentials,
                is_active=access.is_active,
            )
            for access in accesses
        ]

    async def get_access(self, access_id: int) -> AccessDTO:
        access = await self.access_repo.get_by_id(access_id)

        if not access:
            raise AccessNotFoundError(access_id)

        return AccessDTO(
            id=access.id,
            name=access.name,
            description=access.description,
            resource_id=access.resource_id,
            credentials=access.credentials,
            is_active=access.is_active,
        )

    async def delete_access(self, access_id: int):
        deleted = await self.access_repo.delete(access_id)

        if not deleted:
            raise AccessNotFoundError(access_id)
