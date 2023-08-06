import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
admin_id = os.getenv("ADMIN_ID")

from core.youtube.services import check_update, delete_saved_mp3, get_mp3_from_youtube


async def get_start(message: Message):
    await message.answer(f"Привет {message.from_user.full_name}")


async def start_bot(bot: Bot):
    """Отправка уведомления о старте бота"""
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


async def stop_bot(bot: Bot):
    """Отправка уведомления об остоновке бота"""
    await bot.send_message(chat_id=admin_id, text="Бот остановлен")


async def send_mp3(message: Message, bot: Bot):
    """Отправка mp3"""
    try:
        audio = get_mp3_from_youtube(message.text)
        await bot.send_audio(message.chat.id, audio=audio)
        delete_saved_mp3(audio.__dict__["path"])
    except Exception:
        await bot.send_message(
            message.chat.id, text="Неверный адрес, попробуйте еще раз"
        )


async def send_new_youtube_video_from_channel(message: Message, bot: Bot):
    await bot.send_message(message.chat.id, text="Неверный адрес, попробуйте еще раз")


async def get_help(message: Message, bot: Bot):
    """"""
    check_update(message.text)
    await bot.send_message(chat_id=message.chat.id, text="Помощь в разработке")


async def get_settings(message: Message, bot: Bot):
    """"""
    await bot.send_message(chat_id=message.chat.id, text="Настройки в разработке")


async def start():
    """"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )
    bot = Bot(token=token, parse_mode="HTML")

    dp = Dispatcher()

    dp.message.register(get_start, Command(commands=["run", "start"]))
    dp.message.register(get_help, Command(commands=["help"]))
    dp.message.register(get_settings, Command(commands=["settings"]))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(send_mp3)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
