from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import logger
from app.core.shutdown import shutdown
from app.core.startup import startup

@asynccontextmanager
async def lifespan(app:FastAPI):

    logger.info("Starting application")


    startup()
    
    yield # before this code run is startup after this code run in shutdown
    
    shutdown()



    