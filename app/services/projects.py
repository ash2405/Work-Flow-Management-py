from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.schemas.projects import ProjectCreate
from app.db.models import Project
from app.repository.project import( 
create_project, 
get_all_project, 
get_project_by_user, 
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
async def get_user_project_list_service(
        db:AsyncSession,
        user_id:int
): return await get_project_by_user(
        db,user_id
    )

# get all project list
async def get_all_project_list_service(
        db:AsyncSession
): return await get_all_project(db)

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
      data: Project,
      project_id :int,
      db:AsyncSession
):
   project_item =  await get_project_detail_by_id(db,project_id)

   if project_item is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="Project not found"
      )
   
   return await update_project_detail(db,project_item,data)

# delete project 
async def delete_project_service(
    db: AsyncSession,
    project_id: int):

    project = await get_project_detail_by_id(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    await delete_project(
        db=db,
        project=project,
    )

    return {
        "message": "Project deleted successfully.",
        "project_id": project_id,
    }