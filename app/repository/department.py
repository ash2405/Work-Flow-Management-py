from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select,func
from sqlalchemy.orm import selectinload

from app.db.models.user import User
from app.schemas.department import DepartmentRequest
from app.db.models import Department

# create new department
async def create_department(
        department:DepartmentRequest,
        db:AsyncSession
)-> Department:
    new_department = Department(
        name=department.name.strip().lower(),
        description = department.description
    )
    db.add(new_department)
    return new_department

# get user detail by name
async def department_get_by_name_or_id(
        db:AsyncSession,
        department_name:str | None = None,
        department_id:int | None = None
)-> Department:
    query = select(Department)

    if department_name is not None:
        query =  query.where(func.lower(Department.name) == func.lower(department_name))

    if department_id is not None:
       query =  query.where(Department.id == department_id).options(
          selectinload(Department.users).
          selectinload(User.projects)
             )

    department = await db.execute(query)

    return department.scalar_one_or_none()

# get department list
async def get_all_department(
        db:AsyncSession
)->list[Department]: 
    result = await db.execute(
    select(Department)
    )
    return list(result.scalars().all())

# update the department
async def update_department_item(
        data:DepartmentRequest,
        db:AsyncSession,
        department:Department
):
    update_departmnet = data.model_dump(
        exclude_unset= True
    )
    for field,value in update_departmnet.items():
        setattr(department,field,value)

    await db.commit()
    await db.refresh(department)

    return department

# delete department
async def delete_department(
        db:AsyncSession,
        department:Department
): return await db.delete(department)

# get user by departmnet id
async def get_user_list(
        db:AsyncSession,
        department_id:int
):
    user_list = await db.execute(
        select(User).where(User.department_id == department_id)
    )
    return list(user_list.scalars().all())
