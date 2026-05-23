from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.resource import Resource, ResourceCreate
from app.domain.repositories.resource_repository import IResourceRepository
from app.infrastructure.logging.logger import get_logger
from app.infrastructure.persistence.sqlalchemy.models.resource import ResourceORM

logger = get_logger(__name__)


class SQLAlchemyResourceRepository(IResourceRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain_model(self, orm_model: ResourceORM) -> Resource:
        return Resource(
            id=orm_model.id,
            name=orm_model.name,
            type=orm_model.type,
            attributes=orm_model.attributes,
            is_active=orm_model.is_active,
        )

    def _to_orm_model(self, domain_model: Resource | ResourceCreate) -> ResourceORM:
        if isinstance(domain_model, ResourceCreate):
            return ResourceORM(
                name=domain_model.name,
                type=domain_model.type,
                attributes=domain_model.attributes or {},
                is_active=domain_model.is_active,
            )
        return ResourceORM(
            id=domain_model.id,
            name=domain_model.name,
            type=domain_model.type,
            attributes=domain_model.attributes or {},
            is_active=domain_model.is_active,
        )

    def _apply_limit_offset(self, query: Select, limit: int, offset: int) -> Select:
        """Применяет пагинацию к SQL-запросу."""
        query_pagination = query.limit(limit).offset(offset)
        return query_pagination

    async def get_by_id(self, resource_id: int) -> Resource | None:
        orm_resource = await self.db_session.get(ResourceORM, resource_id)
        if orm_resource is None:
            return None
        return self._to_domain_model(orm_resource)

    async def get_all(self, limit: int | None, offset: int) -> list[Resource]:
        stmt = select(ResourceORM)
        if limit:
            stmt = self._apply_limit_offset(stmt, limit, offset)
        result = await self.db_session.execute(stmt)
        resources = result.scalars().all()
        return [self._to_domain_model(resource) for resource in resources]

    async def get_by_name_and_type(self, name: str, type: str) -> Resource | None:
        orm_resource = await self.db_session.scalar(
            select(ResourceORM).where(ResourceORM.name == name, ResourceORM.type == type)
        )

        if orm_resource is None:
            return None

        return self._to_domain_model(orm_resource)

    async def create(self, resource: ResourceCreate) -> Resource:
        orm_resource = self._to_orm_model(resource)
        try:
            self.db_session.add(orm_resource)
            await self.db_session.commit()
            await self.db_session.refresh(orm_resource)
            logger.info('Ресурс успешно создан!')
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(f'Ошибка при создании {orm_resource.__class__.__name__}: {error}')
            raise

        return self._to_domain_model(orm_resource)

    async def update(self, resource: Resource) -> Resource:
        orm_resource = await self.db_session.get(ResourceORM, resource.id)

        if orm_resource is None:
            raise RuntimeError(f'Resource {resource.id} not found during update')

        orm_resource.name = resource.name
        orm_resource.type = resource.type
        orm_resource.attributes = resource.attributes
        orm_resource.is_active = resource.is_active

        try:
            await self.db_session.commit()
            await self.db_session.refresh(orm_resource)
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(
                'Произошла ошибка при обновлении данных в '
                f'{orm_resource.__class__.__name__}: {error}!'
            )
            raise

        return self._to_domain_model(orm_resource)

    async def delete(self, resource_id: int) -> bool:
        orm_resource = await self.db_session.get(ResourceORM, resource_id)

        if orm_resource is None:
            return False

        try:
            await self.db_session.delete(orm_resource)
            await self.db_session.commit()
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(
                'Произошла ошибка при удалении данных из '
                f'{orm_resource.__class__.__name__}: {error}!'
            )
            raise
        return True
