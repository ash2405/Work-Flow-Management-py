from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime
from datetime import datetime, timezone

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user import User


class Department(Base):
    __tablename__ = 'departments'

    id : Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )

    name : Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
        
    )

    description : Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    users : Mapped[list['User']] = relationship(
        back_populates='department'
    )

    created_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default= datetime.now(timezone.utc),
        nullable= False
    )

    updated_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    )
    