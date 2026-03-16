import json
import logging
import os
from datetime import datetime

from app.core.config import settings

LOG_FILE = "logs/app.log"

os.makedirs("logs", exist_ok=True)


class JSONFormatter(logging.Formatter):

    def format(self, record):

        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }

        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)

        if hasattr(record, "correlation_id"):
            log_record["correlation_id"] = record.correlation_id

        # Include extra fields
        if hasattr(record, "method"):
            log_record["method"] = record.method

        if hasattr(record, "path"):
            log_record["path"] = record.path

        if hasattr(record, "status_code"):
            log_record["status_code"] = record.status_code

        if hasattr(record, "process_time_ms"):
            log_record["process_time_ms"] = record.process_time_ms

        if hasattr(record, "client_ip"):
            log_record["client_ip"] = record.client_ip

        return json.dumps(log_record)


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)

    # Show INFO logs always (recommended for APIs)
    logger.setLevel(logging.INFO)

    if not logger.handlers:

        # for console output
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())

        # for file output
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(JSONFormatter())

        logger.addHandler(handler)
        logger.addHandler(file_handler)
        logger.propagate = False

    return logger
