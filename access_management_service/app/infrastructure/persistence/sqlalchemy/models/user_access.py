from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.access import AccessORM


class UserAccessORM(Base):
    user_id: Mapped[int] = mapped_column(nullable=False)
    access_id: Mapped[int] = mapped_column(ForeignKey('accessorm.id'), nullable=False)

    access: Mapped['AccessORM'] = relationship()

    __table_args__ = (UniqueConstraint('user_id', 'access_id', name='uq_user_access'),)
