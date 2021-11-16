import asyncio
from logger import init_logger
from logger.decorators import track_log, LoggerClass


@track_log(init_logger=True)
async def a(logger: LoggerClass):
    logger.warning("a: starting logger")
    await b()


@track_log()
async def b(logger: LoggerClass):
    logger.warning("b: using logger")
    await c()


async def c():
    print("c: no logger or decorator")
    await d()


@track_log()
async def d(logger: LoggerClass):
    logger.warning("d: getting logger from b")


if __name__ == '__main__':
    init_logger()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(a())
