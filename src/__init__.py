import logging

GLOBAL_LOGGER = None


def init_logger(logger_name):
    global GLOBAL_LOGGER
    GLOBAL_LOGGER = logging.getLogger(logger_name)
