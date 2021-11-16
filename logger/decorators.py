import inspect
import time
from functools import wraps

from .logger import LoggerClass
from .prettifiers import prettify
from .exceptions import LoggerNotFound
from . import GLOBAL_CONFIG


def track_log(
        init_logger=False,
        create_if_not_exist=True,
        logging_keys=None,
        search_depth=20,
        log_execution_time=True,
        log_exception=True
):

    def decorator(func):
        arg_spec = inspect.getfullargspec(func)
        args_names = set(arg_spec.args)
        kwargs_names = set(arg_spec.kwonlyargs)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal init_logger, create_if_not_exist, search_depth, logging_keys, log_exception, log_exception, func

            if init_logger:
                search_depth = 0

            logger = __get_logger_from_func(create_if_not_exist, search_depth, logging_keys, func)
            __save_logger_to_func(logger)

            if "logger" in args_names:
                args = (logger, *args)
                __set_logging_keys(logger, func, logging_keys)

            elif "logger" in kwargs_names:
                kwargs["logger"] = logger
                __set_logging_keys(logger, func, logging_keys)

            try:
                if log_execution_time:
                    start = time.time()

                    response = await func(*args, **kwargs)

                    end = time.time()
                    logger.info(f"finished after={end - start} with output={prettify(response)}")

                    return response

                return await func(*args, **kwargs)

            except BaseException as e:
                if log_exception:
                    logger.info(f"{type(e).__name__} exception={e}")

                raise e

        return wrapper

    return decorator


def __save_logger_to_func(logger: LoggerClass) -> None:
    current = inspect.currentframe().f_back
    current.f_locals["logger"] = logger


def __get_logger_from_func(create_if_not_exits, search_depth, logging_keys, func) -> LoggerClass:
    logger = None
    depth = 0
    caller_wrapper = inspect.currentframe().f_back.f_back
    while not logger and depth < search_depth and caller_wrapper:
        logger = caller_wrapper.f_locals.get("logger")
        depth += 1
        caller_wrapper = caller_wrapper.f_back

    if not logger:
        if create_if_not_exits:
            if not logging_keys and not GLOBAL_CONFIG.logging_keys:
                raise ValueError("Not able to construct logger: No logger found and no logging keys provided")

            logger = LoggerClass()

        else:
            raise LoggerNotFound()

    return logger


def __set_logging_keys(logger, func, logging_keys=None):
    if not logging_keys:
        logging_keys = GLOBAL_CONFIG.logging_keys

    for key in logging_keys:
        key = key.lower()
        if key == "module_name":
            logger.extra[key] = func.__module__.split(".")[-1].title()
        elif key == "function_name":
            logger.extra[key] = "-".join(func.__name__.split("_")).title()
