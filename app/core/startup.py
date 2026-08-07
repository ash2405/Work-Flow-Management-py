from app.core.logger import logger
from app.core.config import settings

def startup():
    logger.info(f"Stating {settings.APP_NAME} v{settings.APP_VERSION}")
