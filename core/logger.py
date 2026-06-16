import json
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from core.config.settings import settings

# Calculate the absolute path of the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class StructuredJsonFormatter(logging.Formatter):
    "Custom formatter to serialize log records into JSON format"

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        # Inject exception details if an error occurred
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        # Type-safe extraction of dynamic extra fields to resolve linter warnings
        extra_metadata = getattr(record, "extra_fields", None)
        if isinstance(extra_metadata, dict):
            log_obj.update(extra_metadata)

        return json.dumps(log_obj, ensure_ascii=False)


def setup_logging():
    "Configures structured, production-grade JSON logging with log rotation"
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "geoai_platform.log"

    print(f"Preparing to write JSON logs to absolute path: {log_file}")

    # Replace string formatter with the structured JSON formatter
    json_formatter = StructuredJsonFormatter()

    # 1. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)

    # 2. File Handler (Retaining the existing file rotation mechanism)
    file_handler = RotatingFileHandler(
        filename=str(log_file),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(json_formatter)

    # Get root logger and configure
    root_logger = logging.getLogger()
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(level)

    # Forcefully clear any hidden default handlers, then attach ours
    root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    root_logger = logging.getLogger()
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    third_party_loggers = ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]

    third_party_loggers = ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]

    for logger_name in third_party_loggers:
        ext_logger = logging.getLogger(logger_name)
        ext_logger.handlers.clear()
        ext_logger.addHandler(console_handler)
        ext_logger.addHandler(file_handler)
        ext_logger.propagate = False

    logging.info(
        "Structured JSON Logging initialized successfully.",
        extra={"extra_fields": {"log_level": settings.LOG_LEVEL}},
    )
