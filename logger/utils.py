import re
import sys
from logging import FileHandler
from logging import Formatter
from logging import getLogger
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def _build_stream(config):
    stream = config.get("output")
    if stream:
        handler = StreamHandler(stream=stream)
    else:
        handler = StreamHandler(stream=sys.stdout)

    return handler


def _build_file(config):
    return FileHandler(filename=config.get("output"))


def _build_timed(config):
    return TimedRotatingFileHandler(
        filename=config.get("output"),
        when=config.get("when"),
        interval=config.get("interval"),
        backupCount=config.get("backupCount")
    )


def _build_rotating(config):
    return RotatingFileHandler(
        filename=config.get("output"),
        backupCount=config.get("backupCount")
    )


handler_builder = {
    "stream": _build_stream,
    "file": _build_file,
    "timed": _build_timed,
    "rotating": _build_rotating
}

default_config = {
    "name": "Logger",
    "handler": "stream",
    "output": sys.stdout,
    "format": " [{module_name}/{function_name}] "
}


def build_logger(config=None):
    name = config.get("name")
    handler_type = config.get("handler")
    if not handler_type:
        handler_type = "stream"

    log_format = config.get("format")
    if not log_format:
        log_format = ""

    logger = getLogger(name)
    if handler_type.lower() in handler_builder:
        handler = handler_builder[handler_type.lower()](config)
    else:
        raise ValueError(f"Unknown handler type provided: {config.get('handler')}")

    formatter = Formatter("{levelname:<8}    [{unique_id}] " + log_format + " :  {message}", style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_logging_keys(log_format):
    output = []

    matches = re.finditer(r"\{(.*?)\}", log_format, re.MULTILINE)
    for match in matches:
        for group in match.groups():
            output.append(group.lower())

    return output
