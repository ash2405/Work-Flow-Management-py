from fastapi import APIRouter

from app.routes.auth import router as auth_router
from app.routes.healthcheck import router as health_check_router
from app.routes.projects import router as project_router
from app.routes.user import router as user_router
from app.routes.department import router as department_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(health_check_router)
api_router.include_router(project_router)
api_router.include_router(user_router)
api_router.include_router(department_router)