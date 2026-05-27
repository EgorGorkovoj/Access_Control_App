from sqlalchemy.exc import IntegrityError

from app.application.dtos.access_request_dto import (
    AccessRequestDTO,
    AccessRequestStatusHistoryDTO,
    AccessRequestWithHistoryDTO,
    CreateAccessRequestDTO,
)
from app.application.exceptions.access import AccessNotFoundError
from app.application.exceptions.access_request import (
    RequestAlreadyExistsError,
    RequestNotFoundError,
)
from app.application.exceptions.groups import GroupNotExistsError
from app.domain.models.access_request import AccessRequest, RequestStatus, TargetType
from app.domain.repositories.access_repository import IAccessRepository
from app.domain.repositories.access_request_repository import IAccessRequestRepository
from app.domain.repositories.group_repository import IRightGroupRepository


class AccessRequestService:
    def __init__(
        self,
        access_request_repo: IAccessRequestRepository,
        group_repo: IRightGroupRepository,
        access_repo: IAccessRepository,
    ):
        self.access_request_repo = access_request_repo
        self.group_repo = group_repo
        self.access_repo = access_repo

    async def create_request(self, dto: CreateAccessRequestDTO) -> AccessRequestDTO:
        request = await self.access_request_repo.get_by_request_id(dto.request_id)
        if request is not None:
            raise RequestAlreadyExistsError(request.request_id)
        if dto.target_type == TargetType.GROUP:
            group_id = dto.target_id
            access_id = None
            group = await self.group_repo.get_by_id(group_id)
            if group is None:
                raise GroupNotExistsError(group_id)
        else:
            group_id = None
            access_id = dto.target_id
            access = await self.access_repo.get_by_id(access_id)
            if access is None:
                raise AccessNotFoundError(access_id)
        request = AccessRequest(
            request_id=dto.request_id,
            user_id=dto.user_id,
            access_id=access_id,
            group_id=group_id,
            current_status=RequestStatus.PENDING,
        )
        try:
            created = await self.access_request_repo.create(request)
        except IntegrityError:
            raise RequestAlreadyExistsError(dto.request_id)

        return AccessRequestDTO(
            request_id=created.request_id,
            user_id=created.user_id,
            access_id=created.access_id,
            group_id=created.group_id,
            current_status=created.current_status,
        )

    async def get_all_request_id(self, limit: int | None, offset: int) -> list[str]:
        request_ids = await self.access_request_repo.get_all_request_id(limit=limit, offset=offset)
        return request_ids

    async def get_request(self, request_id: str) -> AccessRequestDTO:
        request = await self.access_request_repo.get_by_request_id(request_id)

        if request is None:
            raise RequestNotFoundError(request_id)

        return AccessRequestDTO(
            request_id=request.request_id,
            user_id=request.user_id,
            access_id=request.access_id,
            group_id=request.group_id,
            current_status=request.current_status,
        )

    async def get_request_with_history(self, request_id: str) -> AccessRequestWithHistoryDTO:
        result = await self.access_request_repo.get_with_history(request_id)

        if result is None:
            raise RequestNotFoundError(request_id)

        request = result.request
        status_history = result.status_history

        return AccessRequestWithHistoryDTO(
            request_id=request.request_id,
            user_id=request.user_id,
            access_id=request.access_id,
            group_id=request.group_id,
            current_status=request.current_status,
            status_history=[
                AccessRequestStatusHistoryDTO(
                    status=history.status,
                    changed_at=history.changed_at,
                    changed_by=history.changed_by,
                )
                for history in status_history
            ],
        )

    async def update_status(
        self,
        request_id: str,
        status: RequestStatus,
        changed_by: int | None = None,
    ) -> None:
        request = await self.access_request_repo.get_by_request_id(request_id)

        if request is None:
            raise RequestNotFoundError(request_id)

        if request.current_status == status:
            return

        await self.access_request_repo.change_status(
            request_id=request_id,
            status=status,
            changed_by=changed_by,
        )
