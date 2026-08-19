from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.dependency import get_db , get_current_user, require_role
from app.services.user import (
                            get_user_by_id_service,
                            get_all_user_service,
                            user_update_service,
                            delete_user_service,
                            active_user)
from app.schemas.user import (  UserListResponse,
                                UserDetail,
                                DeleteUserRequest,
                                UserDetailResponse,
                                UserStatusUpdate)
from app.db.models import User

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('/{user_id}', response_model= UserListResponse)
async def get_user_by_id(
    user_id:int,
    db: AsyncSession= Depends(get_db),
    current_user = Depends(get_current_user)
):

    user = await get_user_by_id_service(db=db,user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get('/',response_model=list[UserListResponse])
async def get_users(
    current_user = Depends(require_role('admin')),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_user_service(db)

# update user
@router.patch('/{user_id}',response_model=UserDetailResponse)
async def update_user(
    user_id:int,
    data:UserDetail,
    db: AsyncSession = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    user = await user_update_service(db, user_id ,data )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# delete user
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    data:DeleteUserRequest | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    ),
):
    return await delete_user_service(
        db=db,
        data=data,
        user_id=user_id,
    )

# user active
@router.patch('/status/{user_id}',response_model=UserStatusUpdate)
async def user_activate(
     user_id:int,
     data:UserStatusUpdate,
     db: AsyncSession= Depends(get_db),
     current_user = Depends(require_role('admin'))
):
     print('c',current_user)
     user = await active_user(
          db=db,
          data=data,
          user_id=user_id
     )

     if user is None:
                 raise HTTPException(
                     status_code=status.HTTP_404_NOT_FOUND,
                     detail="User not found"
                 )
     return user