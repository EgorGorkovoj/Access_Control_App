from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.group_access import GroupAccessORM
    from app.infrastructure.persistence.sqlalchemy.models.user_group import UserGroupORM


class RightGroupORM(Base):
    name: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    accesses: Mapped[list['GroupAccessORM']] = relationship(
        back_populates='group', cascade='all, delete-orphan'
    )

    users: Mapped[list['UserGroupORM']] = relationship(
        back_populates='group', cascade='all, delete-orphan'
    )
