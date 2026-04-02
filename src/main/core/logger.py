from logging import getLogger, INFO, DEBUG, ERROR, WARNING
import logging

logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(logging.StreamHandler())
logger.info("Logger initialized")