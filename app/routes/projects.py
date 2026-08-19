from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency import get_db, get_current_user
from app.schemas.projects import ProjectCreate ,ProjectListResponse, ProjectResponse, ProjectSortField, SortOrder 
from app.db.models.user import User
from app.services.projects import (
    create_project_service, 
    get_project_list_service,
    get_project_detail_service,
    update_project_detail_service,
    delete_project_service
    )

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
@router.get('/',response_model=ProjectListResponse)
async def get_project_list_route(
    limit:int=Query(10,ge=1,le=100),
    page:int=Query(1,ge=1),
    search:str | None = Query(None, min_length=1),
    sort_by: ProjectSortField = Query(ProjectSortField.created_at),
    sort_order: SortOrder = Query(SortOrder.desc),
    db: AsyncSession= Depends(get_db),
    current_user:User= Depends(get_current_user)
):

    return await get_project_list_service(
        db,
        current_user=current_user,
        limit=limit,
        page=page,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
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
    return await update_project_detail_service(data,project_id,db,user=current_user)

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
        project_id=project_id,
        user=current_user
    )