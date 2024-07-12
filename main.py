import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DB_URL, REDIS_URL, TOKEN, CHECK_UPDATE_INTERVAL
from core.bot.handlers import user
from core.bot.middlewares.db_connection import DbConnection
from core.bot.middlewares.long_operation import LongOperationMiddleware
from core.bot.middlewares.throttling import ThrottlingMiddleware
from core.bot.utils import admin_notification
from core.bot.utils.apsheduler import check_video_update


async def start():
    """"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )
    engine = create_async_engine(url=DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    storage = RedisStorage.from_url(REDIS_URL)

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    sheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    sheduler.add_job(
        check_video_update,
        trigger="interval",
        seconds=CHECK_UPDATE_INTERVAL,
        kwargs={"bot": bot, "sessionmaker": sessionmaker},
    )
    sheduler.start()

    dp.message.middleware(ThrottlingMiddleware(storage=storage))
    dp.message.middleware(LongOperationMiddleware())
    dp.update.middleware(DbConnection(sessionmaker))

    dp.include_routers(user.router, admin_notification.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, sessionmaker=sessionmaker)


if __name__ == "__main__":
    asyncio.run(start())
