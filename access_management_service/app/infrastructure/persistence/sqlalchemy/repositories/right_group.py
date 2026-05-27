from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.right_group import RightGroup
from app.domain.repositories.group_repository import IRightGroupRepository
from app.infrastructure.logging.logger import get_logger
from app.infrastructure.persistence.sqlalchemy.models.right_group import RightGroupORM

logger = get_logger(__name__)


class SQLAlchemyRightGroupRepository(IRightGroupRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain_model(self, orm_model: RightGroupORM) -> RightGroup:
        return RightGroup(id=orm_model.id, name=orm_model.name, description=orm_model.description)

    def _to_orm_model(self, domain_model: RightGroup) -> RightGroupORM:
        return RightGroupORM(
            id=domain_model.id, name=domain_model.name, description=domain_model.description
        )

    def _apply_limit_offset(self, query: Select, limit: int, offset: int) -> Select:
        """Applies pagination to an SQL query."""
        query_pagination = query.limit(limit).offset(offset)
        return query_pagination

    async def get_by_id(self, group_id: int) -> RightGroup | None:
        orm_group = await self.db_session.get(RightGroupORM, group_id)
        if orm_group is None:
            return None
        return self._to_domain_model(orm_group)

    async def get_all(self, limit: int | None, offset: int) -> list[RightGroup]:
        stmt = select(RightGroupORM)
        if limit:
            stmt = self._apply_limit_offset(stmt, limit, offset)
        result = await self.db_session.execute(stmt)
        groups = result.scalars().all()
        return [self._to_domain_model(group) for group in groups]

    async def get_by_name(self, group_name: str) -> RightGroup | None:
        orm_group = await self.db_session.scalar(
            select(RightGroupORM).where(RightGroupORM.name == group_name)
        )
        if orm_group is None:
            return None
        return self._to_domain_model(orm_group)

    async def create(self, group: RightGroup) -> RightGroup:
        db_right_group_orm = self._to_orm_model(group)
        try:
            self.db_session.add(db_right_group_orm)
            await self.db_session.commit()
            await self.db_session.refresh(db_right_group_orm)
            logger.info('Permission group successfully created!')
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(
                'An error occurred while creating data in  '
                f'{db_right_group_orm.__class__.__name__}: {error}!'
            )
            raise

        return self._to_domain_model(db_right_group_orm)

    async def update(self, group: RightGroup) -> RightGroup:
        orm_group = await self.db_session.get(RightGroupORM, group.id)

        if orm_group is None:
            raise RuntimeError(f'Resource {group.id} not found during update')

        orm_group.name = group.name
        orm_group.description = group.description

        try:
            await self.db_session.commit()
            await self.db_session.refresh(orm_group)
        except SQLAlchemyError as error:
            logger.error(
                'An error occurred while updating data in '
                f'{orm_group.__class__.__name__}: {error}!'
            )
            raise

        return self._to_domain_model(orm_group)

    async def delete(self, group_id: int) -> bool:
        orm_group = await self.db_session.get(RightGroupORM, group_id)

        if orm_group is None:
            return False

        try:
            await self.db_session.delete(orm_group)
            await self.db_session.commit()
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(
                'An error occurred while deleting data from ' f'{RightGroup.__name__}: {error}!'
            )
            raise
        return True
