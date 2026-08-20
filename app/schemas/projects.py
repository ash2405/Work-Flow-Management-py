from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum
class ProjectCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=500,
    )

class ProjectResponse(ProjectCreate):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProjectListResponse(BaseModel):
    projects: list[ProjectResponse]
    total:int

class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=500,
    )

class ProjectSortField(str, Enum):
    name = "name"
    created_at = "created_at"
    updated_at = "updated_at"
    description = "description"
    
class SortOrder(str,Enum):
    asc = 'asc'
    desc = 'desc'

