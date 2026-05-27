from sqlalchemy import case, or_, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.group_conflict import GroupConflict
from app.domain.repositories.group_conflict_repository import IGroupConflictRepository
from app.infrastructure.logging.logger import get_logger
from app.infrastructure.persistence.sqlalchemy.models.group_access import GroupAccessORM
from app.infrastructure.persistence.sqlalchemy.models.group_conflict import GroupConflictORM

logger = get_logger(__name__)


class SQLAlchemyGroupConflictRepository(IGroupConflictRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain_model(self, orm_model: GroupConflictORM) -> GroupConflict:
        return GroupConflict(
            group_id=orm_model.group_low_id, conflict_group_id=orm_model.group_high_id
        )

    def _to_orm_model(self, domain_model: GroupConflict) -> GroupConflictORM:
        low_id, high_id = domain_model.normalized()
        return GroupConflictORM(group_low_id=low_id, group_high_id=high_id)

    async def get_conflicting_group_ids(self, group_id: int) -> list[int]:
        """Returns a list of group IDs that conflict with the current one."""
        result = await self.db_session.execute(
            select(
                case(
                    (GroupConflictORM.group_low_id == group_id, GroupConflictORM.group_high_id),
                    else_=GroupConflictORM.group_low_id,
                )
            ).where(
                or_(
                    GroupConflictORM.group_low_id == group_id,
                    GroupConflictORM.group_high_id == group_id,
                )
            )
        )
        return list(result.scalars().all())

    async def get_conflicting_accesses_for_groups(
        self,
        group_ids: list[int],
    ) -> list[int]:
        conflict_group = case(
            (
                GroupConflictORM.group_low_id.in_(group_ids),
                GroupConflictORM.group_high_id,
            ),
            else_=GroupConflictORM.group_low_id,
        )

        stmt = (
            select(GroupAccessORM.access_id)
            .join(
                GroupConflictORM,
                or_(
                    GroupConflictORM.group_low_id == GroupAccessORM.group_id,
                    GroupConflictORM.group_high_id == GroupAccessORM.group_id,
                ),
            )
            .where(
                or_(
                    GroupConflictORM.group_low_id.in_(group_ids),
                    GroupConflictORM.group_high_id.in_(group_ids),
                ),
                GroupAccessORM.group_id == conflict_group,
            )
            .distinct()
        )

        result = await self.db_session.execute(stmt)

        return result.scalars().all()

    async def create(self, group_conflict: GroupConflict) -> GroupConflict:
        group_conflict_orm = self._to_orm_model(group_conflict)

        try:
            self.db_session.add(group_conflict_orm)
            await self.db_session.commit()
            logger.info('Conflicting groups successfully created!')
        except IntegrityError:
            await self.db_session.rollback()
            logger.warning('Conflict already exists!')
            raise
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(f'Error creating conflicting groups: {error}')
            raise

        return self._to_domain_model(group_conflict_orm)

    async def delete(self, group_conflict: GroupConflict) -> bool:
        low, high = group_conflict.normalized()

        group_conflict_orm = await self.db_session.get(
            GroupConflictORM, {'group_low_id': low, 'group_high_id': high}
        )

        if group_conflict_orm is None:
            return False

        try:
            await self.db_session.delete(group_conflict_orm)
            await self.db_session.commit()
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(f'Error deleting group conflict: {error}')
            raise

        return True
