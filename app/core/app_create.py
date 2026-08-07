
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logger import logger
from app.core.lifespan import lifespan

from app.api.healthcheck import router as health_check_router

def create_app():
    app = FastAPI(
    title = settings.APP_NAME,
    version = settings.APP_VERSION,
    debug = settings.DEBUG,
    lifespan = lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    )

    app.include_router(health_check_router)
    
    return app

   