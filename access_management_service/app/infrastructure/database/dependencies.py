from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.right_group_service import RightGroupService
from app.domain.repositories.group_repository import IRightGroupRepository
from app.infrastructure.database.connection import AsyncSessionLocal
from app.infrastructure.persistence.sqlalchemy.repositories.right_group import (
    SQLAlchemyRightGroupRepository,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    """Асинхронная зависимость FastAPI для получения сессии SQLAlchemy."""
    async with AsyncSessionLocal() as async_session:
        yield async_session


def get_post_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IRightGroupRepository:
    """Зависимость для предоставления конкретной реализации IRightGroupRepository"""
    return SQLAlchemyRightGroupRepository(db_session)


def get_right_group_service_impl(
    group_repo: IRightGroupRepository = Depends(get_post_repository_impl),
) -> RightGroupService:
    """Зависимость для предоставления RightGroupService"""
    return RightGroupService(group_repo=group_repo)
