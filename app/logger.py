import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import settings

LOG_FORMAT = " %(levelname)s %(name)s  | %(message)s | %(asctime)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }

    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        return super().format(record)


def setup_logging() -> None:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    console_formatter = ColoredFormatter(
        "%(levelname)s  %(message)s  |  %(name)s  |  %(asctime)s",
        datefmt=DATE_FORMAT,
    )


    file_formatter = logging.Formatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    console = logging.StreamHandler()
    console.setFormatter(console_formatter)

    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=5 * 1024 * 1024,   # 5 MB, then rotate
        backupCount=3,              # keep app.log.1, .2, .3, delete older
        encoding="utf-8",
    )   
    file_handler.setFormatter(file_formatter)
    
    root = logging.getLogger()
    root.setLevel(settings.LOG_LEVEL.upper())
    root.handlers.clear()
    root.addHandler(console)
    root.addHandler(file_handler)
    # if settings.LOG_LEVEL:
    #     logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)