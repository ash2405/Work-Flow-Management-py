import sys
from loguru import logger

def setup_logger()-> None:

    # Remove default logger to use custom logger
    # if not remove then duplicate logger will come
    logger.remove()

    # Custom logger
    logger.add(
        sys.stdout, # to show log in console
        level = 'INFO', # TRACE | DEBUG | INFO | SUCCESS | WARNING | ERROR | CRITICAL
        format = (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | " # log time
                "<level>{level: <8}</level> | " # level
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | " # module name, line number and function
                "<level>{message}</level>" # logger.info("Server Started")
                ), # it decides how the log will show
        colorize = True
    )

    # File logger
    logger.add(
        "logs/app.log",
        level="INFO",
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        enqueue=True, # Thread-safe logging.
        backtrace=True,
        diagnose=True,
    )

