import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base, PreBase


class RequestStatus(StrEnum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    APPROVED = 'approved'
    REJECTED = 'rejected'


# TODO: Обновить ERD
# Основная таблица заявок
class AccessRequestORM(Base):
    request_id: Mapped[str] = mapped_column(
        String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(nullable=False)
    access_id: Mapped[int] = mapped_column(ForeignKey('accessorm.id'), nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('rightgrouporm.id'), nullable=True)

    current_status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False
    )

    # история изменений статусов
    status_history: Mapped[list['AccessRequestStatusHistoryORM']] = relationship(
        back_populates='request', cascade='all, delete-orphan'
    )


# Таблица истории статусов
class AccessRequestStatusHistoryORM(PreBase):
    __tablename__ = 'access_request_status_history'

    request_id: Mapped[int] = mapped_column(ForeignKey('accessrequestorm.id'), primary_key=True)
    changed_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), primary_key=True
    )
    status: Mapped[RequestStatus] = mapped_column(Enum(RequestStatus), nullable=False)
    changed_by: Mapped[int | None] = mapped_column(nullable=True)

    request: Mapped['AccessRequestORM'] = relationship(back_populates='status_history')
