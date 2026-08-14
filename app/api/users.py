from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
async def get_users(
    db: AsyncSession = Depends(get_db),
):
    return {
        "message": "Users endpoint",
    }