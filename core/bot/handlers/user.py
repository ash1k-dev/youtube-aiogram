from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN
from core.bot.keyboards.reply import get_main_menu
from core.youtube.services import delete_saved_mp3, get_mp3_from_youtube


bot = Bot(token=TOKEN, parse_mode="HTML")
router = Router()


@router.message(Command(commands=["run", "start"]))
async def get_start(message: Message):
    """Greetings"""
    await message.answer(
        f"Привет {message.from_user.full_name}", reply_markup=get_main_menu()
    )


@router.message(flags={"long_operation": "upload_document"})
async def send_mp3(message: Message, bot: Bot):
    """Receiving url and sending mp3"""
    try:
        audio = get_mp3_from_youtube(message.text)
        await bot.send_audio(message.chat.id, audio=audio)
        delete_saved_mp3(audio.__dict__["path"])
    except Exception:
        await bot.send_message(
            message.chat.id, text="Неверный адрес, попробуйте еще раз"
        )


@router.message()
async def send_new_youtube_video_from_channel(message: Message):
    await message.answer_audio(text="Неверный адрес, попробуйте еще раз")


@router.message(Command(commands=["help"]))
async def get_help(message: Message):
    """"""
    await message.answer(text="Помощь в разработке")


@router.message(Command(commands=["settings"]))
async def get_settings(message: Message):
    """"""
    await message.answer(text="Настройки в разработке")
