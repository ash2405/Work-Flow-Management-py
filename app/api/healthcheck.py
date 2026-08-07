from app.core.logger import logger
from app.core.config import settings
from fastapi import APIRouter

from fastapi.responses import JSONResponse

router = APIRouter(
    tags=['health check']
)

router.get('/',
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
