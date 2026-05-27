from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class PreBase(AsyncAttrs, DeclarativeBase):
    pass


class Base(PreBase):
    """
    Base abstract model for the project.

    Automatically assigns database table names to subclasses
    using the lowercase model name.
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    created_on: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_on: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
