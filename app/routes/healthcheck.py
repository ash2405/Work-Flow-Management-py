from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text


from app.core.logger import logger
from app.core.config import settings
from app.db.database import AsyncSessionLocal

router = APIRouter(
    tags=['health check']
)

@router.get('/',
           summary='Health Check',
           description="Returns the application health status.")
def health_check():

    logger.info('Health Check endpoint is running.')

    return JSONResponse(
        status_code=200,
        content={
            "success":True,
            "message":f"{settings.APP_NAME} is running.",
            "version": f"On Version v{settings.APP_VERSION}"
        }
    )

@router.get("/db",
            summary="DB connection",
            description="check db connection")
async def database_health_check():
    async with AsyncSessionLocal() as session:

        result = await session.execute(text("SELECT 1"))

        return {
            "success": True,
            "database": result.scalar(),
        }
