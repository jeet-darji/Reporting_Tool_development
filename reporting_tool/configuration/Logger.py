import logging
import os
from dotenv import load_dotenv

load_dotenv()
log_path = os.getenv("LOG_PATH")
path = os.path.abspath(os.path.join(log_path))


class Logger:
    def __init__(self):
        if not os.path.exists(path):
            os.makedirs(path)

    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        filehandler = logging.FileHandler(path+"/logs.txt", 'a')
        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03dZ %(levelname)s [reporting-tool-development] [] [%(process)d] [%(processName)s] ['
            '%(threadName)s] - %(name)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        return logger
