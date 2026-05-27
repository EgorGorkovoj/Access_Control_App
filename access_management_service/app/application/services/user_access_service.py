from app.application.dtos.user_access_dto import UserAccessDTO
from app.application.exceptions.access import AccessNotFoundError
from app.domain.models.user_access import UserAccess
from app.domain.repositories.access_repository import IAccessRepository
from app.domain.repositories.user_access_repository import (
    IUserAccessRepository,
)


class UserAccessService:
    def __init__(self, user_access_repo: IUserAccessRepository, access_repo: IAccessRepository):
        self.user_access_repo = user_access_repo
        self.access_repo = access_repo

    async def add_access_user(self, user_id: int, access_id: int) -> UserAccessDTO:
        access = await self.access_repo.get_by_id(access_id=access_id)
        if access is None:
            raise AccessNotFoundError(access_id)
        user_access = UserAccess(user_id=user_id, access_id=access_id)
        created = await self.user_access_repo.add_access(user_access)
        return UserAccessDTO(
            user_id=created.user_id,
            access_id=created.access_id,
        )

    async def remove_access_user(self, user_id: int, access_id: int) -> None:
        deleted = await self.user_access_repo.remove_access(user_id=user_id, access_id=access_id)

        if not deleted:
            raise ValueError(f'User {user_id} does not have access {access_id}')

    async def get_user_accesses(self, user_id: int) -> list[int]:
        """
        Get a user's direct access permissions.
        """
        return await self.user_access_repo.get_all_user_accesses(user_id)
