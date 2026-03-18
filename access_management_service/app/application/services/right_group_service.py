from app.application.dtos.group_dto import CreateRightGroupDTO, RightGroupDTO, UpdateRightGroupDTO
from app.application.exceptions.groups import GroupAlreadyExistsError, GroupNotExistsError
from app.domain.models.right_group import RightGroup
from app.domain.repositories.group_repository import IRightGroupRepository


class RightGroupService:
    def __init__(self, group_repo: IRightGroupRepository):
        self.group_repo = group_repo

    async def get_right_group(self, group_id: int) -> RightGroupDTO | None:
        group = await self.group_repo.get_by_id(group_id)
        if group is None:
            raise GroupNotExistsError(group_id)
        return RightGroupDTO(
            id=group.id,
            name=group.name,
            description=group.description,
        )

    async def get_right_groups(self, limit: int | None, offset: int) -> list[RightGroupDTO]:
        groups = await self.group_repo.get_all(limit, offset)
        return [
            RightGroupDTO(
                id=group.id,
                name=group.name,
                description=group.description,
            )
            for group in groups
        ]

    async def create_right_group(self, dto: CreateRightGroupDTO) -> RightGroupDTO:
        existing_group = await self.group_repo.get_by_name(dto.name)
        if existing_group:
            raise GroupAlreadyExistsError(dto.name)
        domain_model = RightGroup(
            name=dto.name,
            description=dto.description,
        )
        created_group = await self.group_repo.create(domain_model)
        return RightGroupDTO(
            id=created_group.id,
            name=created_group.name,
            description=created_group.description,
        )

    async def update_right_group(self, dto: UpdateRightGroupDTO) -> RightGroupDTO:
        domain_model = RightGroup(
            id=dto.id,
            name=dto.name,
            description=dto.description,
        )
        updated = await self.group_repo.update(domain_model)

        if updated is None:
            raise GroupNotExistsError(dto.id)

        return RightGroupDTO(
            id=updated.id,
            name=updated.name,
            description=updated.description,
        )

    async def delete_right_group(self, group_id: int) -> None:
        deleted = await self.group_repo.delete(group_id)
        if not deleted:
            raise GroupNotExistsError(group_id)
