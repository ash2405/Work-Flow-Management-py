
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
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

    return {"message": "User registered successfully.", "user": user}


@router.post('/login',
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
                 detail="Invalid Email and Password."
              )

    return Auth.AuthResponse(
        user=user,
        message="User Logged in"
    )

@router.post('/refresh',response_model=Auth.TokenResponse)
async def refresh_token(data:Auth.RefreshToken):
    return await refresh_access_token(data.refresh_token)

@router.post("/token")
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # Swagger's "username" field contains the user's email
    data = Auth.LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    token_data = await login_request(
        db=db,
        data=data,
    )

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email and Password",
        )

    return {
        "access_token": token_data["access_token"],
        "token_type": "bearer",
    }