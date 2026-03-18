from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.right_group import RightGroupORM


class UserGroupORM(Base):
    user_id: Mapped[int] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('rightgrouporm.id'), nullable=False)

    group: Mapped['RightGroupORM'] = relationship(back_populates='users')

    __table_args__ = (UniqueConstraint('user_id', 'group_id', name='uq_user_group'),)
