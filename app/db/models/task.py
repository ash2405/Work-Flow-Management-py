
from datetime import datetime, timezone

from sqlalchemy import String, Text, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from enum import Enum


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status : Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus),
        default=TaskStatus.TODO,
        nullable=False

    )

    priority : Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority),
        default=TaskPriority.LOW,
        nullable=False
    )

    project_id : Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    assign_to : Mapped[int | None] = mapped_column(
        ForeignKey('users.id'),
        nullable=True
    )

    created_by : Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=True
    )

    due_date : Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    ) 

    assignee : Mapped["User| None"] = relationship(
        foreign_keys=[assign_to],
        back_populates='assigned_tasks'
    )

    creator : Mapped['User'] = relationship(
        foreign_keys=[created_by],
        back_populates='created_tasks'
    )

    project : Mapped["Project"] = relationship(
        back_populates='tasks'
    )