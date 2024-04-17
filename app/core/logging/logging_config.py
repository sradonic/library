import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from app.core.config import settings


def close_loggers():
    for handler in logging.root.handlers[:]:
        handler.close()
        logging.root.removeHandler(handler)


def setup_logging():
    if not settings.log_to_file:
        return None
    close_loggers()
    log_dir = "logs"
    log_file_name = "application.log"
    log_file_path = os.path.join(log_dir, log_file_name)
    archive_dir = os.path.join(log_dir, "archive")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if os.path.isfile(log_file_path):
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)
        creation_time = os.path.getctime(log_file_path)
        formatted_time = datetime.fromtimestamp(creation_time).strftime('%Y%m%d_%H%M%S%f')
        archived_file_name = f"{log_file_name}_{formatted_time}.log"
        archived_file_path = os.path.join(archive_dir, archived_file_name)

        counter = 1
        while os.path.exists(archived_file_path):
            archived_file_name = f"{log_file_name}_{formatted_time}_{counter}.log"
            archived_file_path = os.path.join(archive_dir, archived_file_name)
            counter += 1

        os.rename(log_file_path, archived_file_path)

    logger = logging.getLogger("library_api")
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(log_file_path, maxBytes=10 ** 6, backupCount=10, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
