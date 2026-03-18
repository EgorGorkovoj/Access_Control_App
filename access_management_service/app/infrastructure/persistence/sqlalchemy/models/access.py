from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.group_access import GroupAccessORM
    from app.infrastructure.persistence.sqlalchemy.models.resource import ResourceORM


class AccessORM(Base):
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text)
    resource_id: Mapped[int] = mapped_column(ForeignKey('resourceorm.id'), nullable=False)

    resource: Mapped['ResourceORM'] = relationship(back_populates='accesses')
    groups: Mapped[list['GroupAccessORM']] = relationship(back_populates='access')
