from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.schemas.projects import ProjectCreate, ProjectSortField, ProjectUpdate, SortOrder
from app.db.models import Project, User
from app.repository.project import( 
create_project, 
get_all_project, 
get_project_detail_by_id,
update_project_detail,
delete_project
)

# create project by logged in user
async def create_project_service(
        db: AsyncSession,
        data: ProjectCreate,
        user_id:int
):
    project = Project(
        name = data.name,
        description = data.description,
        owner_id = user_id
    )

    return await create_project(
        db,project
    )

# get project list
async def get_project_list_service(
        db:AsyncSession,
        current_user:User,        
        limit:int = 10,
        page:int = 1,
        search:str|None = None,
        sort_order: SortOrder = SortOrder.desc ,
        sort_by : ProjectSortField = ProjectSortField.created_at,
): 
       projects , total = await get_all_project(
               db,
               current_user=current_user,
               limit=limit,
               page=page,
               search=search,
               sort_order=sort_order,
               sort_by=sort_by
            ) 
       return {
           "projects":projects,
           "total":total
       }

# get project detail
async def get_project_detail_service(
        db:AsyncSession,
        project_id:int
):
 detail =  await get_project_detail_by_id(db,  project_id)

 if detail is None:
    raise HTTPException(
       status_code=status.HTTP_404_NOT_FOUND,
       detail="No Project found."
    )
 return detail

# update project detail
async def update_project_detail_service(
      data: ProjectUpdate,
      project_id :int,
      db:AsyncSession,
      user:User
):
   project_item =  await get_project_detail_by_id(db,project_id)


   if project_item is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="Project not found"
      )
   
   if project_item.owner_id != user.id and user.role != 'admin':
      raise HTTPException(
         status_code=status.HTTP_403_FORBIDDEN,
         detail="Only Project owner can update"
      )
   
   return await update_project_detail(db,project_item,data)

# delete project 
async def delete_project_service(
    db: AsyncSession,
    project_id: int,
    user:User):

    project = await get_project_detail_by_id(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    
    if project.owner_id != user.id and user.role != 'admin':
        raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN,
           detail="Only Project owner or admin can delete"
        )

    await delete_project(
        db=db,
        project=project,
    )

    return {
        "message": "Project deleted successfully.",
        "project_id": project_id,
    }