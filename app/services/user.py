from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repository.user import (
                            get_user_by_id,
                            get_all_user,
                            update_user_detail,
                            delete_user
                            )
from app.db.models import User
from app.schemas.user import DeleteUserRequest

# get user detail by id
async def get_user_by_id_service(
        db:AsyncSession,
        user_id:int
):
    user_detail = await get_user_by_id(db=db,user_id=int(user_id))

    if user_detail is None:
        None

    return user_detail

# get all users
async def get_all_user_service(
        db:AsyncSession,
       
): return await get_all_user(db)

# update user
async def user_update_service(
        db:AsyncSession,
        user_id:int,
        data:User
):

    user = await get_user_by_id(db,user_id)
    if user is None:
        raise None

    return await update_user_detail(db,data,user)

async def delete_user_service(
    db: AsyncSession,
    user_id: int,
    data: DeleteUserRequest
):
    # get user to delete id
    user = await get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        # if user has project then get transfer user
        if data and data.transfer_to_user_id and len(user.projects) != 0:

            if data.transfer_to_user_id == user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot transfer projects to the same user",
                )

            transferUser = await get_user_by_id(
                                                db=db,
                                                user_id=data.transfer_to_user_id)

            if transferUser is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Transfer User not found"
                )

            for project in user.projects:
                 project.owner_id = transferUser.id

        else:
            for project in user.projects:
              await  db.delete(project)

            # await update_user_detail(db,transferUser,transferUser)

        await delete_user(
                db=db,
                user=user,
            )
        
        await db.commit()

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise    
  

    return {
        "message": "User deleted successfully.",
        "user_id": user_id,
    }

# set user active
async def active_user(
        db:AsyncSession,
        data:User,
        user_id:int
):
    user = await get_user_by_id(db, user_id)

    if user is None:
        None
        
    return await update_user_detail(db, data,user)