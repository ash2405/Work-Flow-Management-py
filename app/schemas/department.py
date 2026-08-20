from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from app.schemas.user import UserUpdateDetailResponse

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

class DepartmentDetailResponse(DepartmentRequest):
    id : int
    created_at : datetime
    users:list[UserUpdateDetailResponse]
    model_config = ConfigDict(from_attributes=True)
    