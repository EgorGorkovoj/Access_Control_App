from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.access_service import AccessService
from app.application.services.group_access_service import GroupAccessService
from app.application.services.group_conflict_service import GroupConflictService
from app.application.services.resource_service import ResourceService
from app.application.services.right_group_service import RightGroupService
from app.domain.repositories.access_repository import IAccessRepository
from app.domain.repositories.group_access_repository import IGroupAccessRepository
from app.domain.repositories.group_conflict_repository import IGroupConflictRepository
from app.domain.repositories.group_repository import IRightGroupRepository
from app.domain.repositories.resource_repository import IResourceRepository
from app.infrastructure.database.connection import AsyncSessionLocal
from app.infrastructure.persistence.sqlalchemy.repositories.access import (
    SQLAlchemyAccessRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.group_access import (
    SQLAlchemyGroupAccessRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.group_conflict import (
    SQLAlchemyGroupConflictRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.resource import (
    SQLAlchemyResourceRepository,
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
    """Зависимость для предоставления конкретной реализации IGroupConflictRepository"""
    return SQLAlchemyGroupConflictRepository(db_session)


def get_group_conflict_service_impl(
    group_conflict_repo: IGroupConflictRepository = Depends(
        get_right_group_conflict_repository_impl
    ),
    group_repo: IRightGroupRepository = Depends(get_right_group_repository_impl),
) -> GroupConflictService:
    """Зависимость для предоставления GroupConflictService"""
    return GroupConflictService(conflict_repo=group_conflict_repo, group_repo=group_repo)


def get_resource_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IResourceRepository:
    """Зависимость для предоставления конкретной реализации IResourceRepository"""
    return SQLAlchemyResourceRepository(db_session)


def get_resource_service_impl(
    resource_repo: IResourceRepository = Depends(get_resource_repository_impl),
) -> ResourceService:
    """Зависимость для предоставления ResourceService"""
    return ResourceService(resource_repo=resource_repo)


def get_access_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IAccessRepository:
    """Зависимость для предоставления конкретной реализации IAccessRepository"""
    return SQLAlchemyAccessRepository(db_session)


def get_access_service_impl(
    access_repo: IAccessRepository = Depends(get_access_repository_impl),
    resource_repo: IResourceRepository = Depends(get_resource_repository_impl),
) -> AccessService:
    """Зависимость для предоставления AccessService."""
    return AccessService(access_repo=access_repo, resource_repo=resource_repo)


def get_group_access_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IGroupAccessRepository:
    """Зависимость для предоставления конкретной реализации IGroupAccessRepository."""
    return SQLAlchemyGroupAccessRepository(db_session)


def get_group_access_service_impl(
    group_access_repo: IGroupAccessRepository = Depends(get_group_access_repository_impl),
    group_repo: IRightGroupRepository = Depends(get_right_group_repository_impl),
    access_repo: IAccessRepository = Depends(get_access_repository_impl),
) -> GroupAccessService:
    """Зависимость для предоставления GroupAccessService."""
    return GroupAccessService(
        group_access_repo=group_access_repo, group_repo=group_repo, access_repo=access_repo
    )
