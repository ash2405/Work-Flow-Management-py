from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.schemas.department import (
                DepartmentRequest, 
                DepartmentResponse,
                DepartmentDetailResponse)
from app.core.dependency import get_db, require_role, get_current_user
from app.services.department import (
                            create_department_service, 
                            get_department_detail,
                            department_list,
                            update_department,
                            delete_department_item
                            )

router = APIRouter(
    prefix='/department',
    tags=['Department']
    )
# create new department 
@router.post('/',response_model=DepartmentResponse)
async def create_department(
    data:DepartmentRequest,
    db:AsyncSession = Depends(get_db),
    current_user = Depends(require_role('admin'))   
): return await create_department_service(db=db, data=data)

# get detail by department id
@router.get('/{department_id}',response_model=DepartmentDetailResponse)
async def departmnet_detail(
    department_id:int,
    db:AsyncSession= Depends(get_db),
    current_user = Depends(require_role('admin'))
): return await get_department_detail(db=db,department_id=department_id)

# get all department list
@router.get('/',response_model=list[DepartmentResponse])
async def get_department_list(
    db:AsyncSession = Depends(get_db),
    curretn_user = Depends(get_current_user)
): return await department_list(db=db)

# update department item
@router.patch('/{deaprtment_id}',response_model=DepartmentResponse)
async def update_department_item(
    department_id:int,
    data:DepartmentRequest,
    db:AsyncSession=Depends(get_db),
    current_user = Depends(require_role('admin'))
):
    return await update_department(db=db,department_id=department_id,data=data)

# delete department
@router.delete('/{department_id}')
async def delete_item(
    department_id:int,
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role('admin'))
): return await delete_department_item(db=db,department_id=department_id)
    