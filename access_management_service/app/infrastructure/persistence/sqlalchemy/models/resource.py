from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from infrastructure.persistence.sqlalchemy.models.access import AccessORM


class ResourceORM(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    attributes: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    accesses: Mapped[list['AccessORM']] = relationship(
        back_populates='resource', cascade='all, delete-orphan'
    )

    __table_args__ = (UniqueConstraint('name', 'type', name='uq_resource_name_type'),)
