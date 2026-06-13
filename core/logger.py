import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from core.config.settings import settings

# Calculate the absolute path of the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def setup_logging():
    "Configures structured, production-grade logging with log rotation."
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "geoai_platform.log"

    # Debug print to show EXACTLY where the file is being created
    print(f"Preparing to write logs to absolute path: {log_file}")

    # Define a standard format for logs
    log_format = logging.Formatter(
        fmt=(
            "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] "
            "%(message)s"
        ),
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    # 1. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)

    # 2. File Handler
    file_handler = RotatingFileHandler(
        filename=str(log_file),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_format)

    # Get root logger and configure
    root_logger = logging.getLogger()
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(level)

    # THE FIX: Forcefully clear any hidden default handlers, then attach ours
    root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Silence noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logging.info(f"Logging initialized successfully at {settings.LOG_LEVEL} level.")
