import logging.handlers

__all__ = ("enable_file_logging",)

LOGFILE = "pymino.log"
MAX_LOG_SIZE = 10 * 1024 * 1024

logger = logging.getLogger("pymino")
logger.addHandler(logging.NullHandler())


def enable_file_logging(level: int = logging.DEBUG) -> None:
    handler = logging.handlers.RotatingFileHandler(
        LOGFILE, maxBytes=MAX_LOG_SIZE, encoding="utf-8"
    )
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
