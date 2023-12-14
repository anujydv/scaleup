import http
from fastapi import HTTPException
import logging
from src.config.config import settings
from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(JsonFormatter, self).add_fields(log_record, record, message_dict)
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        log_record['timestamp'] = timestamp
        if log_record.get('level'):
            log_record['level'] = record.levelname
        if log_record.get('message'):
            log_record['message'] = record.getMessage()
        if log_record.get('module'):
            log_record['module'] = record.module
        if log_record.get('status_code'):
            log_record['status_code'] = record.status_code
        if 'asctime' in log_record:
            del log_record['asctime']


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(
            settings.DEVELOPMENT.LOGGING.LOGGING_NAME)
        if not self.logger.handlers:
            self.logger.setLevel(settings.DEVELOPMENT.LOGGING.LOGGING_LEVEL)
            logHandler = logging.StreamHandler()
            formatter = JsonFormatter(
                '%(timestamp)s %(levelname)s %(name)s %(message)s %(module)s %(status_code)s')
            logHandler.setFormatter(formatter)
            self.logger.addHandler(logHandler)

    def get_logger(self):
        return self.logger


class ScaleupError(HTTPException):
    """ scaleup server error """

    def __init__(self, status_code: int, error: str = None) -> None:  # pylint: disable=super-init-not-called
        if error is None:
            error = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.error = error

    def __repr__(self) -> str:
        return f"(status_code={self.status_code!r}, error={self.error!r})"
