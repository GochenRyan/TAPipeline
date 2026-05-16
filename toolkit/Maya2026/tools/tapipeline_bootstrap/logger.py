import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

_LOGGER_NAME = "tapipeline"
_INITIALIZED = False


def _log_dir() -> str:
    base = os.environ.get("TAPIPELINE_LOG_DIR")
    if base:
        return base
    docs = os.path.join(os.path.expanduser("~"), "Documents", "maya", "2026", "logs")
    return docs


def get_logger() -> logging.Logger:
    return logging.getLogger(_LOGGER_NAME)


def init() -> logging.Logger:
    global _INITIALIZED
    logger = get_logger()
    if _INITIALIZED:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    log_dir = _log_dir()
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"tapipeline_{datetime.now():%Y%m%d}.log")

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter("[TAPipeline] %(message)s"))
    logger.addHandler(stream_handler)

    _INITIALIZED = True
    logger.info("Logger initialized, writing to %s", log_file)
    return logger
