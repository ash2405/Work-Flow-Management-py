from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.db.models import User
from app.core.security import decode_access_token
from app.repository.auth import get_user_by_id

# Get token from header authentication
outh2_password = OAuth2PasswordBearer(
    tokenUrl='/auth/login'
)

# For creating the session for every request and after completing it the session will close
async def get_db()-> AsyncGenerator[AsyncSessionLocal,None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
        token:str = Depends(outh2_password),
        db: AsyncSession = Depends(get_db)
)-> User:
    # decode the jwt token
    payload = decode_access_token(token)

    # get user id from jwt token object
    user_id = payload.get('sub')

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # get user from table with user id
    user = get_user_by_id(user_id)


    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


def require_role(*required_role:str):
    async def role_checker(
            current_user:User = Depends(get_current_user)
    )->User:

        if current_user.role not in required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource"
            )

        return current_user

    return role_checker