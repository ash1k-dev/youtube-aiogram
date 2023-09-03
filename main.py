import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from core.bot.handlers import user
from core.bot.utils import admin_notification

from core.bot.middlewares.long_operation import LongOperationMiddleware
from core.bot.middlewares.check_authorization import CheckAuthorization


async def start():
    """"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )
    bot = Bot(token=TOKEN, parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.message.middleware(LongOperationMiddleware())
    dp.message.middleware(CheckAuthorization())

    dp.include_routers(user.router, admin_notification.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
