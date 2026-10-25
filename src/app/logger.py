"""Shared logger: `from app.logger import logger`. Writes to stderr at INFO."""

import logging

LOG_FORMAT = "%(levelname)s %(module)s: %(message)s"

_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.addHandler(_handler)
