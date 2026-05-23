from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.group_access import GroupAccess
from app.domain.repositories.group_access_repository import IGroupAccessRepository
from app.infrastructure.logging.logger import get_logger
from app.infrastructure.persistence.sqlalchemy.models.group_access import GroupAccessORM

logger = get_logger(__name__)


class SQLAlchemyGroupAccessRepository(IGroupAccessRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain(self, orm: GroupAccessORM) -> GroupAccess:
        return GroupAccess(group_id=orm.group_id, access_id=orm.access_id)

    def _to_orm_model(self, domain: GroupAccess) -> GroupAccessORM:
        return GroupAccessORM(group_id=domain.group_id, access_id=domain.access_id)

    async def create(self, group_access: GroupAccess) -> GroupAccess:
        orm_group_access = self._to_orm_model(group_access)

        try:
            self.db_session.add(orm_group_access)
            await self.db_session.commit()
            await self.db_session.refresh(orm_group_access)
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(f'Ошибка создания данных в {orm_group_access.__name__}: {error}!')
            raise

        return self._to_domain(orm_group_access)

    async def exists(self, group_id: int, access_id: int) -> bool:
        result = await self.db_session.scalar(
            select(GroupAccessORM).where(
                GroupAccessORM.group_id == group_id, GroupAccessORM.access_id == access_id
            )
        )
        if result is None:
            return False
        return True

    async def delete(self, group_id: int, access_id: int) -> bool:
        group_access_orm = await self.db_session.scalar(
            select(GroupAccessORM).where(
                GroupAccessORM.group_id == group_id, GroupAccessORM.access_id == access_id
            )
        )

        if group_access_orm is None:
            return False

        try:
            await self.db_session.delete(group_access_orm)
            await self.db_session.commit()
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(f'Ошибка при удалении данных из {group_access_orm.__name__}: {error}!')
            raise

        return True

    async def get_by_group_id(self, group_id: int) -> list[int]:
        group_access_orm = await self.db_session.execute(
            select(GroupAccessORM.access_id).where(GroupAccessORM.group_id == group_id)
        )
        return group_access_orm.scalars().all()
