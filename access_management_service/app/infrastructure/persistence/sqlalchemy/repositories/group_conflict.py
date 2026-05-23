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
        """Преобразует SQLAlchemy ORM-модель в чистую доменную модель."""
        return GroupConflict(
            group_id=orm_model.group_low_id, conflict_group_id=orm_model.group_high_id
        )

    def _to_orm_model(self, domain_model: GroupConflict) -> GroupConflictORM:
        """Преобразует чистую доменную модель в SQLAlchemy ORM-модель."""
        low_id, high_id = domain_model.normalized()
        return GroupConflictORM(group_low_id=low_id, group_high_id=high_id)

    # async def get_by_group_id(self, group_conflict_id: int) -> list[GroupConflict]:
    #     result = await self.db_session.execute(
    #         select(GroupConflictORM).where(
    #             or_(
    #                 GroupConflictORM.group_low_id == group_conflict_id,
    #                 GroupConflictORM.group_high_id == group_conflict_id,
    #             )
    #         )
    #     )

    #     orm_conflicts = result.scalars().all()

    #     return [self._to_domain_model(conflict) for conflict in orm_conflicts]

    async def get_conflicting_group_ids(self, group_id: int) -> list[int]:
        """Возвращает список ID групп, которые конфликтуют с данной"""
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
            logger.info('Конфликтующие группы успешно созданы!')
        except IntegrityError:
            await self.db_session.rollback()
            logger.warning('Конфликт уже существует')
            raise
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error('Ошибка при создании конфликтующих групп: ' f'{error}')
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
            logger.error('Ошибка при удалении конфликта групп: ' f'{error}')
            raise

        return True
