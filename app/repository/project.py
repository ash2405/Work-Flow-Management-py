from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.db.models import Project , User
from app.schemas.projects import ProjectSortField, SortOrder
from app.utils.project_sorting import ProjectSort

# create project by login user
async def create_project(
        db: AsyncSession,
        project: Project
)-> Project:
    
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

# get all project list if admin logged in
async def get_all_project(
    db: AsyncSession,
    current_user: User,
    limit: int = 10,
    page: int = 1,
    search: str | None = None,
    sort_by: ProjectSortField = ProjectSortField.created_at,
    sort_order: SortOrder = SortOrder.desc,
) -> tuple[list[Project], int]:    

    # Calculate offset for pagination
    offset = (page - 1) * limit

    # Base queries
    query = select(Project)
    count_query = select(func.count()).select_from(Project)

    # Apply search filter
    if search:
        search_condition = Project.name.ilike(
            f"%{search}%"
        )

        query = query.where(search_condition)
        count_query = count_query.where(
            search_condition
        )

    # Apply user filter
    if current_user.role != "admin":
        user_condition = (
            Project.owner_id == current_user.id
        )

        query = query.where(user_condition)
        count_query = count_query.where(
            user_condition
        )

    # Determine sort column
    order_column = ProjectSort.get_sort(sort_by)

    # Apply sort order
    if sort_order == SortOrder.desc:
        query = query.order_by(
            order_column.desc()
        )
    else:
        query = query.order_by(
            order_column.asc()
        )

    # Apply pagination
    query = query.offset(offset).limit(limit)

    # Execute project query
    project_result = await db.execute(query)

    # Execute count query
    count_result = await db.execute(count_query)

    # Get projects and total count
    projects = list(
        project_result.scalars().all()
    )

    total = count_result.scalar_one()

    return projects, total

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