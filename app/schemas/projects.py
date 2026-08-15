from pydantic import BaseModel, ConfigDict
from datetime import datetime
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