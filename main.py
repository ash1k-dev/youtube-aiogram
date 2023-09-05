import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# from aiogram.fsm.storage.redis import RedisStorage

from config import TOKEN
from core.bot.handlers import user
from core.bot.utils import admin_notification

from core.bot.middlewares.long_operation import LongOperationMiddleware
from core.bot.middlewares.db_connection import DbConnection
from core.bot.middlewares.check_authorization import CheckAuthorization


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DB_URL


async def start():
    """"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )
    engine = create_async_engine(url=DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=TOKEN, parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.message.middleware(LongOperationMiddleware())
    dp.message.outer_middleware(DbConnection(sessionmaker))
    dp.edited_message.outer_middleware(DbConnection(sessionmaker))
    dp.message.middleware(CheckAuthorization(sessionmaker))

    dp.callback_query.middleware(DbConnection(sessionmaker))

    dp.include_routers(user.router, admin_notification.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, sessionmaker=sessionmaker)


if __name__ == "__main__":
    asyncio.run(start())
