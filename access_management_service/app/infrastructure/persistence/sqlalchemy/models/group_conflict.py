from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.sqlalchemy.models.base import PreBase


class GroupConflictORM(PreBase):
    __tablename__ = 'group_conflicts'

    group_low_id: Mapped[int] = mapped_column(
        ForeignKey('rightgrouporm.id', ondelete='CASCADE'), primary_key=True, nullable=False
    )

    group_high_id: Mapped[int] = mapped_column(
        ForeignKey('rightgrouporm.id', ondelete='CASCADE'), primary_key=True, nullable=False
    )

    __table_args__ = (
        CheckConstraint('group_low_id < group_high_id', name='check_group_conflict_order'),
    )
