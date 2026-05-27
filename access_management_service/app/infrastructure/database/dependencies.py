from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.access_request_service import AccessRequestService
from app.application.services.access_service import AccessService
from app.application.services.group_access_service import GroupAccessService
from app.application.services.group_conflict_service import GroupConflictService
from app.application.services.permissions_management_service import PermissionManagementService
from app.application.services.resource_access_service import ResourceAccessService
from app.application.services.resource_service import ResourceService
from app.application.services.right_group_service import RightGroupService
from app.application.services.user_group_service import UserGroupService
from app.application.services.user_permission_query_service import UserPermissionQueryService
from app.application.services.user_permissions_service import UserPermissionsService
from app.domain.repositories.access_repository import IAccessRepository
from app.domain.repositories.access_request_repository import IAccessRequestRepository
from app.domain.repositories.group_access_repository import IGroupAccessRepository
from app.domain.repositories.group_conflict_repository import IGroupConflictRepository
from app.domain.repositories.group_repository import IRightGroupRepository
from app.domain.repositories.resource_repository import IResourceRepository
from app.domain.repositories.user_access_repository import IUserAccessRepository
from app.domain.repositories.user_group_repository import IUserGroupRepository
from app.infrastructure.database.connection import AsyncSessionLocal
from app.infrastructure.persistence.sqlalchemy.repositories.access import (
    SQLAlchemyAccessRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.access_request import (
    SQLAlchemyAccessRequestRepository,
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
from app.infrastructure.persistence.sqlalchemy.repositories.user_access import (
    SQLAlchemyUserAccessRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.user_group import (
    SQLAlchemyUserGroupRepository,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    """FastAPI async dependency that provides a SQLAlchemy session."""
    async with AsyncSessionLocal() as async_session:
        yield async_session


def get_right_group_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IRightGroupRepository:
    """Dependency that provides a concrete implementation of IRightGroupRepository."""
    return SQLAlchemyRightGroupRepository(db_session)


def get_right_group_service_impl(
    group_repo: IRightGroupRepository = Depends(get_right_group_repository_impl),
) -> RightGroupService:
    """Dependency that provides RightGroupService."""
    return RightGroupService(group_repo=group_repo)


def get_right_group_conflict_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IGroupConflictRepository:
    """Dependency that provides a concrete implementation of IGroupConflictRepository"""
    return SQLAlchemyGroupConflictRepository(db_session)


def get_group_conflict_service_impl(
    group_conflict_repo: IGroupConflictRepository = Depends(
        get_right_group_conflict_repository_impl
    ),
    group_repo: IRightGroupRepository = Depends(get_right_group_repository_impl),
) -> GroupConflictService:
    """Dependency that provides GroupConflictService"""
    return GroupConflictService(conflict_repo=group_conflict_repo, group_repo=group_repo)


def get_resource_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IResourceRepository:
    """Dependency that provides a concrete implementation of IResourceRepository"""
    return SQLAlchemyResourceRepository(db_session)


def get_resource_service_impl(
    resource_repo: IResourceRepository = Depends(get_resource_repository_impl),
) -> ResourceService:
    """Dependency that provides ResourceService"""
    return ResourceService(resource_repo=resource_repo)


def get_access_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IAccessRepository:
    """Dependency that provides a concrete implementation of IAccessRepository"""
    return SQLAlchemyAccessRepository(db_session)


def get_access_service_impl(
    access_repo: IAccessRepository = Depends(get_access_repository_impl),
    resource_repo: IResourceRepository = Depends(get_resource_repository_impl),
) -> AccessService:
    """Dependency that provides AccessService."""
    return AccessService(access_repo=access_repo, resource_repo=resource_repo)


def get_group_access_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IGroupAccessRepository:
    """Dependency that provides a concrete implementation of IGroupAccessRepository."""
    return SQLAlchemyGroupAccessRepository(db_session)


def get_group_access_service_impl(
    group_access_repo: IGroupAccessRepository = Depends(get_group_access_repository_impl),
    group_repo: IRightGroupRepository = Depends(get_right_group_repository_impl),
    access_repo: IAccessRepository = Depends(get_access_repository_impl),
) -> GroupAccessService:
    """Dependency that provides GroupAccessService."""
    return GroupAccessService(
        group_access_repo=group_access_repo, group_repo=group_repo, access_repo=access_repo
    )


def get_user_group_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IUserGroupRepository:
    """Dependency that provides a concrete implementation of IUserGroupRepository."""
    return SQLAlchemyUserGroupRepository(db_session)


def get_user_group_service_impl(
    user_group_repo: IUserGroupRepository = Depends(get_user_group_repository_impl),
    group_repo: IRightGroupRepository = Depends(get_right_group_repository_impl),
) -> UserGroupService:
    """Dependency that provides UserGroupService."""
    return UserGroupService(user_group_repo=user_group_repo, group_repo=group_repo)


def get_access_request_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IAccessRequestRepository:
    """Dependency that provides a concrete implementation of IAccessRequestRepository."""
    return SQLAlchemyAccessRequestRepository(db_session)


def get_access_request_service_impl(
    access_request_repo: IAccessRequestRepository = Depends(get_access_request_repository_impl),
    group_repo: IRightGroupRepository = Depends(get_right_group_repository_impl),
    access_repo: IAccessRepository = Depends(get_access_repository_impl),
) -> AccessRequestService:
    """Dependency that provides AccessRequestService."""
    return AccessRequestService(
        access_request_repo=access_request_repo, group_repo=group_repo, access_repo=access_repo
    )


def get_user_access_repository_impl(
    db_session: AsyncSession = Depends(get_async_session),
) -> IUserAccessRepository:
    """Dependency that provides a concrete implementation of IUserAccessRepository."""
    return SQLAlchemyUserAccessRepository(db_session)


def get_user_permissions_service_impl(
    user_group_repo: IUserGroupRepository = Depends(get_user_group_repository_impl),
    group_conflict_repo: IGroupConflictRepository = Depends(
        get_right_group_conflict_repository_impl
    ),
) -> UserPermissionsService:
    """Dependency that provides UserPermissionsService."""
    return UserPermissionsService(
        user_group_repo=user_group_repo,
        group_conflict_repo=group_conflict_repo,
    )


def get_permissions_management_service_impl(
    user_group_repo: IUserGroupRepository = Depends(get_user_group_repository_impl),
    user_access_repo: IUserAccessRepository = Depends(get_user_access_repository_impl),
    group_repo: IRightGroupRepository = Depends(get_right_group_repository_impl),
    access_repo: IAccessRepository = Depends(get_access_repository_impl),
) -> PermissionManagementService:
    """Dependency that provides PermissionManagementService."""
    return PermissionManagementService(
        user_group_repo=user_group_repo,
        user_access_repo=user_access_repo,
        group_repo=group_repo,
        access_repo=access_repo,
    )


def get_user_permissions_query_service_impl(
    user_group_repo: IUserGroupRepository = Depends(get_user_group_repository_impl),
    group_access_repo: IGroupAccessRepository = Depends(get_group_access_repository_impl),
    user_access_repo: IUserAccessRepository = Depends(get_user_access_repository_impl),
) -> UserPermissionQueryService:
    """Dependency that provides UserPermissionQueryService."""
    return UserPermissionQueryService(
        user_group_repo=user_group_repo,
        group_access_repo=group_access_repo,
        user_access_repo=user_access_repo,
    )


def get_resource_access_service_impl(
    resource_repo: IResourceRepository = Depends(get_resource_repository_impl),
    access_repo: IAccessRepository = Depends(get_access_repository_impl),
) -> ResourceAccessService:
    """Dependency that provides ResourceAccessService."""
    return ResourceAccessService(resource_repo=resource_repo, access_repo=access_repo)
