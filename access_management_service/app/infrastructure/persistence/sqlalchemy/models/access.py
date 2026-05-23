from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.group_access import GroupAccessORM
    from app.infrastructure.persistence.sqlalchemy.models.resource import ResourceORM


class AccessORM(Base):
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey('resourceorm.id'), nullable=False)
    credentials: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    is_active: Mapped[bool] = mapped_column(default=True)

    resource: Mapped['ResourceORM'] = relationship(back_populates='accesses')
    groups: Mapped[list['GroupAccessORM']] = relationship(back_populates='access')

    __table_args__ = (UniqueConstraint('name', 'resource_id', name='uq_access_name_resource'),)
