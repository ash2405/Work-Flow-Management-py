from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repository.department import (
                        department_get_by_name_or_id,
                        create_department, 
                        get_all_department,
                        update_department_item,
                        get_user_list,
                        delete_department)
from app.schemas.department import DepartmentRequest

# create new department
async def create_department_service(
    db: AsyncSession,
    data: DepartmentRequest,
):
    # get department detail by name
    existing_department = await department_get_by_name_or_id(
        db=db,
        department_name=data.name,
    )
    # check is existing for set unique name
    if existing_department is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department name already exists",
        )
    # create new department 
    department = await create_department(
        db=db,
        department=data,
    )
    await db.commit()
    await db.refresh(department)
    return department

# get department detail by id
async def get_department_detail(department_id:int,db:AsyncSession):
    # get detail by id
    department = await department_get_by_name_or_id(db=db,department_id=department_id)

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department is not found"
        )
    return department

# get department list
async def department_list(db:AsyncSession):
    return await get_all_department(db=db)

# update department item
async def update_department(
        db:AsyncSession,
        data:DepartmentRequest,
        department_id:int
):
    # get user item
    department_item = await department_get_by_name_or_id(db=db,department_id=department_id)

    if department_item.name == data.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Same name can't be update"
        )

    if department_item is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Department is not found"
        )
    return await update_department_item(db=db,data=data, department=department_item)

# delete department
async def delete_department_item(
    db:AsyncSession,
    department_id:int
):
    department = await department_get_by_name_or_id(db=db,department_id=department_id)

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    try:
        user_list = await get_user_list(db=db,department_id=department_id)

        for user in user_list:
            user.department_id = None

        await delete_department(db=db,department=department)

        await db.commit()

    except Exception:
        await db.rollback()
        raise
    
    return {
        "message": "Department deleted successfully",
    }
        