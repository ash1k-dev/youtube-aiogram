from aiogram import Bot, Router

router = Router()

from config import ADMIN_ID, TOKEN

bot = Bot(token=TOKEN, parse_mode="HTML")


@router.startup()
async def start_bot(bot: Bot):
    """Sending message about start bot"""
    await bot.send_message(chat_id=ADMIN_ID, text="Бот запущен")


@router.shutdown()
async def stop_bot(bot: Bot):
    """Sending message about stop bot"""
    await bot.send_message(chat_id=ADMIN_ID, text="Бот остановлен")
