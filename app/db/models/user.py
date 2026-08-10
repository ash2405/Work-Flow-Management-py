from sqlalchemy.orm import Mapped, mapped_column , relationship
from sqlalchemy import String, DateTime, Boolean
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.project import Project

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str]= mapped_column(
        String(225),
        index=True,
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(225),
        nullable=False
    )

    is_active: Mapped[Boolean] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    projects: Mapped[list["Project"]] = relationship(
        back_populates="owner"
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )