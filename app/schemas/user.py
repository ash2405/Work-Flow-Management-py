from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.schemas.projects import ProjectResponse

class UserDetailRequest(BaseModel):
    id: int

class UserDetail(BaseModel):
    name: str
    email: str

class UserStatusUpdate(BaseModel):
    is_active: bool

class UserListResponse(UserDetail,UserDetailRequest):
    role: str = 'user'
    is_active: bool
    created_at: datetime
    updated_at: datetime
    department_id:int
    model_config = ConfigDict(
    from_attributes= False
    )

class UserDetailResponse(UserDetail,UserDetailRequest):
    role: str = 'user'
    is_active: bool
    created_at: datetime
    updated_at: datetime
    projects: list[ProjectResponse]
    model_config = ConfigDict(
    from_attributes= False
    )

class DeleteUserRequest(BaseModel):
    transfer_to_user_id : int | None = None