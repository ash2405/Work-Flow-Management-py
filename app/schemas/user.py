from pydantic import BaseModel, ConfigDict, Field
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

class UserUpdateDetailResponse(UserDetail,UserDetailRequest):
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

class UserDetailResponse(UserUpdateDetailResponse):
    department: DepartmentResponse | None = None
    model_config = ConfigDict(
        from_attributes=True
    )

class DepartmentRequest(BaseModel):
    name : str = Field(
        min_length=2,
        max_length=50
    )
    description : str = Field(
        min_length=10,
        max_length=500
    )

class DepartmentResponse(DepartmentRequest):
    id : int
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)