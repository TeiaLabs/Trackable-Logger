import inspect
import time
from functools import wraps

from .logger import LoggerClass
from .prettifiers import prettify


def init_logger(func):
    module_name = func.__module__.split(".")[-1].title()
    function_name = "-".join(func.__name__.split("_")).title()

    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger = LoggerClass(module_name, function_name)

        __save_logger_to_func(logger)

        logger.info("started")
        response = await func(*args, **kwargs)
        logger.info(f"finished")

        return response

    return wrapper


def get_logger(func):
    module_name = func.__module__.split(".")[-1].title()
    function_name = "-".join(func.__name__.split("_")).title()

    arg_spec = inspect.getfullargspec(func)
    args_names = set(arg_spec.args)
    kwargs_names = set(arg_spec.kwonlyargs)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger = __get_logger_from_func()
        logger.module_name = module_name
        logger.function_name = function_name

        __save_logger_to_func(logger)

        # Check if function expects logger as argument or keyword argument
        if "logger" in args_names:
            args = (logger, *args)
        elif "logger" in kwargs_names:
            kwargs["logger"] = logger

        try:
            logger.info("started")
            start = time.time()

            response = await func(*args, **kwargs)

            end = time.time()
            logger.info(f"finished after={end - start} with output={prettify(response)}")

            return response

        except Exception as e:
            logger.info(f"{type(e).__name__} exception={e}")
            raise e

    return wrapper


def __save_logger_to_func(logger: LoggerClass) -> None:
    current = inspect.currentframe().f_back
    current.f_locals["logger"] = logger


def __get_logger_from_func() -> LoggerClass:
    caller_wrapper = inspect.currentframe().f_back.f_back.f_back
    return caller_wrapper.f_locals["logger"]
