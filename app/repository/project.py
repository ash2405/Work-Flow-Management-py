from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Project 
async def create_project(
        db: AsyncSession,
        project: Project
):
    await db.add(project)
    await db.commit()
    await db.refresh(project)

    return project