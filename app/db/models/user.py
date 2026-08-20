from sqlalchemy.orm import Mapped, mapped_column , relationship
from sqlalchemy import String, DateTime, Boolean, ForeignKey
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.project import Project
    from app.db.models.department import Department

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    department_id : Mapped[ int | None] = mapped_column(
        ForeignKey('departments.id'),
        nullable=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="user",
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

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    projects: Mapped[list["Project"]] = relationship(
        back_populates="owner"
    )

    created_at: Mapped[datetime] = mapped_column(
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

    department: Mapped["Department | None"] = relationship(
            back_populates="users"
    )

    assigned_tasks : Mapped[list['Task']]= relationship(
        foreign_keys="Task.assign_to",
        back_populates="assignee"
    )

    created_tasks : Mapped[list["Task"]] = relationship(
        foreign_keys="Task.created_by",
        back_populates="creator"
    )