from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.user_group import UserGroup
from app.domain.repositories.user_group_repository import IUserGroupRepository
from app.infrastructure.logging.logger import get_logger
from app.infrastructure.persistence.sqlalchemy.models.user_group import UserGroupORM

logger = get_logger(__name__)


class SQLAlchemyUserGroupRepository(IUserGroupRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain_model(self, orm: UserGroupORM) -> UserGroup:
        return UserGroup(user_id=orm.user_id, group_id=orm.group_id)

    def _to_orm_model(self, domain_model: UserGroup) -> UserGroupORM:
        """Преобразует чистую доменную модель в SQLAlchemy ORM-модель."""
        return UserGroupORM(user_id=domain_model.user_id, group_id=domain_model.group_id)

    async def create(self, user_group: UserGroup) -> UserGroup:
        user_group_orm = UserGroupORM(user_id=user_group.user_id, group_id=user_group.group_id)
        try:
            self.db_session.add(user_group_orm)
            await self.db_session.commit()
            await self.db_session.refresh(user_group_orm)
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(
                'Произошла ошибка при создании данных в ' f'{user_group_orm.__name__}: {error}!'  # type: ignore
            )
            raise

        return self._to_domain_model(user_group_orm)

    async def exists(self, user_id: int, group_id: int) -> bool:
        result = await self.db_session.scalar(
            select(UserGroupORM).where(
                UserGroupORM.user_id == user_id, UserGroupORM.group_id == group_id
            )
        )
        if result is None:
            return False
        return True

    async def delete(self, user_id: int, group_id: int) -> bool:
        user_group_orm = await self.db_session.scalar(
            select(UserGroupORM).where(
                UserGroupORM.user_id == user_id, UserGroupORM.group_id == group_id
            )
        )

        if user_group_orm is None:
            return False

        try:
            await self.db_session.delete(user_group_orm)
            await self.db_session.commit()
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(f'Ошибка при удалении данных из {user_group_orm.__name__}: {error}!')
            raise

        return True

    async def get_all_by_user_id(self, user_id: int) -> list[int]:
        user_groups_orm = await self.db_session.execute(
            select(UserGroupORM.group_id).where(UserGroupORM.user_id == user_id)
        )
        return user_groups_orm.scalars().all()

    async def get_user_group(self, user_group: UserGroup) -> UserGroup | None:
        stmt = select(UserGroupORM).where(
            UserGroupORM.user_id == user_group.user_id,
            UserGroupORM.group_id == user_group.group_id,
        )

        result = await self.db_session.execute(stmt)

        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        return self._to_domain_model(orm)
