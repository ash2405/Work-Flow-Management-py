from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.projects import ProjectCreate
from app.db.models import Project
from app.repository.project import create_project

async def create_project(
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