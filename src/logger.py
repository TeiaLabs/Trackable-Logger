import logging
import secrets

from . import GLOBAL_LOGGER


class LoggerClass:
    def __init__(self, module_name: str, function_name: str):
        self.module_name = module_name
        self.function_name = function_name
        self.unique_id = secrets.token_urlsafe(10)

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
        GLOBAL_LOGGER.log(level, message, extra=dict(
            resource=self.module_name,
            method=self.function_name,
            unique_id=self.unique_id,
        ))
