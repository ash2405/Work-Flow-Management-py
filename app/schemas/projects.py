from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum
class ProjectCreate(BaseModel):
    name:str
    description: str | None = None

class ProjectResponse(ProjectCreate):
    id: int
    owner_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProjectListResponse(BaseModel):
    projects: list[ProjectResponse]
    total:int

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ProjectSortField(str, Enum):
    name = "name"
    created_at = "created_at"
    updated_at = "updated_at"
    description = "description"
    
class SortOrder(str,Enum):
    asc = 'asc'
    desc = 'desc'

