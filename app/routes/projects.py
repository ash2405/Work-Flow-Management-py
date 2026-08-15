from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency import get_db, get_current_user
from app.schemas.projects import ProjectCreate
from app.db.models.user import User
from app.services.projects import (
    create_project_service, 
    get_user_project_list_service, 
    get_all_project_list_service,
    get_project_detail_service,
    update_project_detail_service,
    delete_project_service
    )
from app.schemas.projects import ProjectResponse
router = APIRouter(
    prefix='/project',
    tags=['Projects']
)

# create new project
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
    return await create_project_service(db,data,current_user.id)

# get project list for user or admin
@router.get('/',response_model=list[ProjectResponse])
async def get_project_list_route(
    db: AsyncSession= Depends(get_db),
    current_user:User= Depends(get_current_user)
):

    if current_user.role == 'admin':
        return await get_all_project_list_service(
                db
            )

    return await get_user_project_list_service(
        db,
        user_id=int(current_user.id)
    )

# get project detail by project id
@router.get('/{project_id}',response_model=ProjectResponse)
async def get_project_detail_route(project_id:int ,
                                   db:AsyncSession = Depends(get_db),
                                   current_user:User= Depends(get_current_user)):
    return await get_project_detail_service(db,project_id)

# update project detail
@router.patch('/{project_id}',response_model= ProjectResponse)
async def update_project(data:ProjectCreate,
                         project_id: int,
                         db:AsyncSession = Depends(get_db),
                         current_user:User=Depends(get_current_user)):
    return await update_project_detail_service(data,project_id,db)

# delete project
@router.delete(
    "/{project_id}",
)
async def delete_project_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_project_service(
        db=db,
        project_id=project_id
    )