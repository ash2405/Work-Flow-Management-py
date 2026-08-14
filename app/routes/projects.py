from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency import get_db, get_current_user
from app.schemas.projects import ProjectCreate
from app.db.models.user import User
from app.services.projects import create_project

router = APIRouter(
    prefix='/project',
    tags=['Projects']
)

@router.post('/')
async def create_project_endpoint (
    data: ProjectCreate,
    db:AsyncSession = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Token has expired"
        )
    return await create_project(db,data,current_user.id)