import logging
import secrets

from . import GLOBAL_CONFIG


class LoggerClass:
    def __init__(self, **extra):
        self.unique_id = secrets.token_urlsafe(10)
        self.extra = {}
        if extra:
            self.extra = extra

    def debug(self, message: str) -> None:
        self._log(logging.DEBUG, message)

    def info(self, message: str) -> None:
        self._log(logging.INFO, message)

    def warning(self, message: str) -> None:
        self._log(logging.WARNING, message)

    def error(self, message: str) -> None:
        self._log(logging.ERROR, message)

    def critical(self, message: str) -> None:
        self._log(logging.CRITICAL, message)

    def _log(self, level: int, message: str) -> None:
        GLOBAL_CONFIG.logger.log(level, message, extra={**self.extra, "unique_id": self.unique_id})
