from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.group_conflict_service import GroupConflictService
from app.application.services.right_group_service import RightGroupService
from app.domain.repositories.group_conflict_repository import IGroupConflictRepository
from app.domain.repositories.group_repository import IRightGroupRepository
from app.infrastructure.database.connection import AsyncSessionLocal
from app.infrastructure.persistence.sqlalchemy.repositories.group_conflict import (
    SQLAlchemyGroupConflictRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.right_group import (
    SQLAlchemyRightGroupRepository,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    """Асинхронная зависимость FastAPI для получения сессии SQLAlchemy."""
    async with AsyncSessionLocal() as async_session:
        yield async_session


def get_right_group_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IRightGroupRepository:
    """Зависимость для предоставления конкретной реализации IRightGroupRepository"""
    return SQLAlchemyRightGroupRepository(db_session)


def get_right_group_service_impl(
    group_repo: IRightGroupRepository = Depends(get_right_group_repository_impl),
) -> RightGroupService:
    """Зависимость для предоставления RightGroupService"""
    return RightGroupService(group_repo=group_repo)


def get_right_group_conflict_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IGroupConflictRepository:
    """Зависимость для предоставления конкретной реализации SQLAlchemyGroupConflictRepository"""
    return SQLAlchemyGroupConflictRepository(db_session)


def get_group_conflict_service_impl(
    group_conflict_repo: IGroupConflictRepository = Depends(
        get_right_group_conflict_repository_impl
    ),
    group_repo: IRightGroupRepository = Depends(get_right_group_repository_impl),
) -> GroupConflictService:
    """Зависимость для предоставления RightGroupService"""
    return GroupConflictService(conflict_repo=group_conflict_repo, group_repo=group_repo)
