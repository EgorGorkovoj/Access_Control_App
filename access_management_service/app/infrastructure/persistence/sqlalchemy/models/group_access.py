from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.access import AccessORM
    from app.infrastructure.persistence.sqlalchemy.models.right_group import RightGroupORM


class GroupAccessORM(Base):
    group_id: Mapped[int] = mapped_column(
        ForeignKey('rightgrouporm.id', ondelete='CASCADE'), nullable=False
    )
    access_id: Mapped[int] = mapped_column(
        ForeignKey('accessorm.id', ondelete='CASCADE'), nullable=False
    )

    group: Mapped['RightGroupORM'] = relationship(back_populates='accesses')
    access: Mapped['AccessORM'] = relationship(back_populates='groups')

    __table_args__ = (UniqueConstraint('group_id', 'access_id', name='uq_group_access'),)
