import logging
import os

def logger_setup():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    logger = logging.getLogger("mylogger")
    logger.setLevel(logging.INFO)

    # Stop logs from going to root logger
    logger.propagate = False

    # File handler
    file_handler = logging.FileHandler("logs/mylogs.log")

    formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger