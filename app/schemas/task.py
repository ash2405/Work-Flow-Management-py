from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Text

from app.db.models.task import TaskPriority , TaskStatus

class CreateTask(BaseModel):
    title : str = Field(min_length=2,max_length=200)
    description =  Text
    status : TaskStatus = TaskStatus.TODO
    priority : TaskPriority = TaskPriority.LOW

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None,min_length=1,max_length=200)
    description: str | None = None
    assign_to: int | None = None
    priority: TaskPriority | None = None
    status: TaskStatus | None = None
    due_date: datetime | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    project_id: int
    assign_to: int | None
    created_by: int
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int