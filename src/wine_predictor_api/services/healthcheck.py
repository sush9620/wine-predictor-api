from typing import Tuple
from wine_predictor_api import logger


def ping() -> Tuple:
    logger.info("Just received a ping")
    return "pong", 200
