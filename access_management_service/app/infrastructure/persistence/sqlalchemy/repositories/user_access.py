from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.user_access import UserAccess
from app.domain.repositories.user_access_repository import IUserAccessRepository
from app.infrastructure.logging.logger import get_logger
from app.infrastructure.persistence.sqlalchemy.models.user_access import UserAccessORM

logger = get_logger(__name__)


class SQLAlchemyUserAccessRepository(IUserAccessRepository):
    def _to_domain_model(self, orm: UserAccessORM) -> UserAccess:
        return UserAccess(user_id=orm.user_id, access_id=orm.access_id)

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_access(self, user_access: UserAccess) -> UserAccess:
        user_access_orm = UserAccessORM(
            user_id=user_access.user_id,
            access_id=user_access.access_id,
        )
        try:
            self.db_session.add(user_access_orm)
            await self.db_session.commit()
            await self.db_session.refresh(user_access_orm)
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(
                'An error occurred while creating data in '
                f'{user_access_orm.__class__.__name__}: {error}!'
            )
            raise
        return self._to_domain_model(user_access_orm)

    async def remove_access(self, user_id: int, access_id: int) -> bool:
        user_access_orm = await self.db_session.scalar(
            select(UserAccessORM).where(
                UserAccessORM.user_id == user_id, UserAccessORM.access_id == access_id
            )
        )
        if user_access_orm is None:
            return False
        try:
            await self.db_session.delete(user_access_orm)
            await self.db_session.commit()
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(
                'An error occurred while deleting data from '
                f' {user_access_orm.__class__.__name__}: {error}!'
            )
            raise

        return True

    async def get_all_user_accesses(
        self,
        user_id: int,
    ) -> list[int]:
        stmt = select(UserAccessORM.access_id).where(UserAccessORM.user_id == user_id)

        result = await self.db_session.execute(stmt)

        return result.scalars().all()
