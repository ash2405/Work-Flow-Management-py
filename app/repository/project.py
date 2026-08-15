from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Project 

# create project by login user
async def create_project(
        db: AsyncSession,
        project: Project
)-> Project:
    
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

# get user project list
async def get_project_by_user(
        db:AsyncSession,
        user_id:int
)-> list[Project]:
    
    project_list = await db.execute(
        select(Project).where(Project.owner_id == user_id)
    )
    return list(project_list.scalars().all())

# get all project list if admin logged in
async def get_all_project(
        db:AsyncSession
)-> list[Project]:
    
    project_list = await db.execute(
        select(Project)
    )
    return list(project_list.scalars().all())

# get project detail
async def get_project_detail_by_id(
        db:AsyncSession,
        project_id:int
)-> Project | None:
    detail = await db.execute(
        select(Project).where(Project.id == project_id)
    )

    return detail.scalar_one_or_none()

# update project detail
async def update_project_detail(
        db:AsyncSession,
        project_detail:Project,
        data:Project
)->Project:

    if data.name is not None:
        project_detail.name = data.name

    if data.description is not None:
        project_detail.description = data.description

    await db.commit()
    await db.refresh(project_detail)

    return project_detail

# delete project
async def delete_project(
    db: AsyncSession,
    project: Project,
):
    await db.delete(project)
    await db.commit()