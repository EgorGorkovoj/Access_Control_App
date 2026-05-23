from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.models.access_request import (
    AccessRequest,
    AccessRequestStatusHistory,
    RequestStatus,
)
from app.domain.repositories.access_request_repository import IAccessRequestRepository
from app.infrastructure.logging.logger import get_logger
from app.infrastructure.persistence.sqlalchemy.models.access_request import (
    AccessRequestORM,
    AccessRequestStatusHistoryORM,
)

logger = get_logger(__name__)


class SQLAlchemyAccessRequestRepository(IAccessRequestRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain_model(self, orm: AccessRequestORM) -> AccessRequest:
        return AccessRequest(
            id=orm.id,
            request_id=orm.request_id,
            user_id=orm.user_id,
            access_id=orm.access_id,
            group_id=orm.group_id,
            current_status=orm.current_status,
        )

    def _to_domain_with_history(self, orm: AccessRequestORM) -> AccessRequest:
        base = self._to_domain_model(orm)

        history = [
            AccessRequestStatusHistory(
                status=stat.status,
                changed_at=stat.changed_at,
                changed_by=stat.changed_by,
            )
            for stat in orm.status_history
        ]

        base.status_history = history
        return base

    def _to_orm_model(self, domain: AccessRequest) -> AccessRequestORM:
        return AccessRequestORM(
            id=domain.id,
            request_id=domain.request_id,
            user_id=domain.user_id,
            access_id=domain.access_id,
            group_id=domain.group_id,
            current_status=domain.current_status,
        )

    async def create(self, access_request: AccessRequest) -> AccessRequest:
        orm = self._to_orm_model(access_request)

        try:
            self.db_session.add(orm)
            await self.db_session.flush()
            history = AccessRequestStatusHistoryORM(
                request_pk=orm.id,
                status=orm.current_status,
                changed_by=None,
            )
            self.db_session.add(history)
            await self.db_session.commit()
            await self.db_session.refresh(orm)
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(f'Ошибка создания {orm.__class__.__name__}: {error}')
            raise
        return self._to_domain_model(orm)

    async def get_with_history(self, request_id: str) -> AccessRequest | None:
        stmt = (
            select(AccessRequestORM)
            .where(AccessRequestORM.request_id == request_id)
            .options(selectinload(AccessRequestORM.status_history))
        )

        result = await self.db_session.execute(stmt)
        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        return self._to_domain_with_history(orm)

    async def get_by_request_id(self, request_id: str) -> AccessRequest | None:
        stmt = select(AccessRequestORM).where(AccessRequestORM.request_id == request_id)

        result = await self.db_session.execute(stmt)
        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        return self._to_domain_model(orm)

    async def change_status(
        self,
        request_id: str,
        status: RequestStatus,
        changed_by: int | None = None,
    ) -> None:
        stmt = select(AccessRequestORM).where(AccessRequestORM.request_id == request_id)
        result = await self.db_session.execute(stmt)
        orm = result.scalar_one_or_none()
        if orm is None:
            return

        try:
            orm.current_status = status
            history = AccessRequestStatusHistoryORM(
                request_pk=orm.id,
                status=status,
                changed_by=changed_by,
            )
            self.db_session.add(history)
            await self.db_session.commit()
        except SQLAlchemyError as error:
            await self.db_session.rollback()
            logger.error(f'Ошибка обновления статуса в {orm.__class__.__name__}: {error}')
            raise
