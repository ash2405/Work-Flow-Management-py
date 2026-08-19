from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import Auth
from app.services.auth import login_request
from app.core.dependency import get_db

router = APIRouter(
    prefix='/token',
    tags=['Token']
)

@router.post("/")
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # Swagger's "username" field contains the user's email
    data = Auth.LoginRequest(
        username=form_data.username,
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