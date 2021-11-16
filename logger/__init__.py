from .utils import Singleton, build_logger, get_logging_keys, default_config


class LoggerConfig(object):
    __metaclass__ = Singleton

    def __init__(self, logger=None, logging_keys=None):
        self.logger = logger
        self.logging_keys = logging_keys


GLOBAL_CONFIG = LoggerConfig()


def init_logger(config=None):
    global GLOBAL_CONFIG

    if config is None:
        config = default_config.copy()

    GLOBAL_CONFIG.logger = build_logger(config)
    GLOBAL_CONFIG.logging_keys = get_logging_keys(config.get("format"))
