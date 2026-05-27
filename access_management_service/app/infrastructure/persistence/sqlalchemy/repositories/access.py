from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.access import Access, AccessCreate
from app.domain.repositories.access_repository import IAccessRepository
from app.infrastructure.logging.logger import get_logger
from app.infrastructure.persistence.sqlalchemy.models.access import AccessORM

logger = get_logger(__name__)


class SQLAlchemyAccessRepository(IAccessRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain_model(self, orm: AccessORM) -> Access:
        return Access(
            id=orm.id,
            name=orm.name,
            description=orm.description,
            resource_id=orm.resource_id,
            credentials=orm.credentials,
            is_active=orm.is_active,
        )

    def _to_orm_model(self, domain: Access | AccessCreate) -> AccessORM:
        if isinstance(domain, AccessCreate):
            return AccessORM(
                name=domain.name,
                description=domain.description,
                resource_id=domain.resource_id,
                credentials=domain.credentials,
                is_active=domain.is_active,
            )
        return AccessORM(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            resource_id=domain.resource_id,
            credentials=domain.credentials,
            is_active=domain.is_active,
        )

    def _apply_limit_offset(self, query: Select, limit: int, offset: int) -> Select:
        """Applies pagination to an SQL query."""
        query_pagination = query.limit(limit).offset(offset)
        return query_pagination

    async def create(self, access: AccessCreate) -> Access:
        orm = self._to_orm_model(access)

        try:
            self.db_session.add(orm)
            await self.db_session.commit()
            await self.db_session.refresh(orm)
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(f'Error creating {orm.__class__.__name__}: {error}')
            raise

        return self._to_domain_model(orm)

    async def get_all(self, limit: int | None, offset: int) -> list[Access]:
        stmt = select(AccessORM)

        if limit:
            stmt = self._apply_limit_offset(stmt, limit, offset)

        result = await self.db_session.execute(stmt)
        accesses = result.scalars().all()
        return [self._to_domain_model(access) for access in accesses]

    async def get_by_id(self, access_id: int) -> Access | None:
        orm_access = await self.db_session.get(AccessORM, access_id)
        if orm_access is None:
            return None
        return self._to_domain_model(orm_access)

    async def get_by_resource_id(self, resource_id: int) -> list[Access]:
        result = await self.db_session.execute(
            select(AccessORM)
            .where(AccessORM.resource_id == resource_id, AccessORM.is_active.is_(True))
            .order_by(AccessORM.name)
        )
        return [self._to_domain_model(access) for access in result.scalars().all()]

    async def get_by_name_and_resource(self, name: str, resource_id: int) -> Access | None:
        orm_access = await self.db_session.scalar(
            select(AccessORM).where(AccessORM.name == name, AccessORM.resource_id == resource_id)
        )
        if not orm_access:
            return None
        return self._to_domain_model(orm_access)

    async def delete(self, access_id: int) -> bool:
        orm_access = await self.db_session.get(AccessORM, access_id)

        if not orm_access:
            return False

        try:
            await self.db_session.delete(orm_access)
            await self.db_session.commit()
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(
                'An error occurred while deleting data from '
                f'{orm_access.__class__.__name__}: {error}!'
            )
            raise
        return True
