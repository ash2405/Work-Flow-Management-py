
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import Auth
from app.core.dependency import get_db
from app.services.auth import singup, login_request, refresh_access_token

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/signup',
             status_code= status.HTTP_201_CREATED)
async def signup_user(
    data:Auth.SignupRequest,
    db:AsyncSession= Depends(get_db)
):
    user = await singup(db,data)

    if user is None:
         raise HTTPException(
                 status_code=400,
                 detail="Email is already exist."
              )
    return {"message": "User registered successfully.", "user": user}


@router.post('/signin',
             status_code=status.HTTP_200_OK,
             response_model=Auth.AuthResponse)
async def login_user(
     data:Auth.LoginRequest,
     db:AsyncSession= Depends(get_db)
):
    user =  await login_request(db,data)

    if user is None:
        raise HTTPException(
                 status_code=401,
                 detail="Password is not matched."
              )

    return Auth.AuthResponse(
        user=user,
        message="User Logged in"
    )

@router.post('/refresh',response_model=Auth.TokenResponse)
async def refresh_token(data:Auth.RefreshToken):
    user_token = await refresh_access_token(data.refresh_token)
    if user_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invaild Resfresh Token"
        )
    return Auth.TokenResponse(
        access_token=user_token,
        token_type="bearer"
    )



    
