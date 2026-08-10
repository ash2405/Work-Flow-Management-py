from sqlalchemy.orm import Mapped, mapped_column, relationship
# below is for data type
from sqlalchemy import ForeignKey, DateTime, String
# below is for convertion
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User

class Project (Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False,
        index=True
    )

    name : Mapped[str] = mapped_column(
        String(225),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        back_populates="projects",
    )