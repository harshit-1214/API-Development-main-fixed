import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import settings

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=5 * 1024 * 1024,   # 5 MB, then rotate
        backupCount=3,              # keep app.log.1, .2, .3, delete older
        encoding="utf-8",
    )   
    file_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(settings.LOG_LEVEL.upper())
    root.handlers.clear()
    root.addHandler(console)
    root.addHandler(file_handler)
    # if settings.LOG_LEVEL:
    #     logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)