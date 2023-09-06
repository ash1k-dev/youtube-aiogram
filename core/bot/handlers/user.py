from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from core.bot.keyboards.reply import get_main_menu
from core.bot.keyboards.inline import get_channels_menu, get_control_menu
from core.youtube.services import delete_saved_mp3, get_mp3_from_youtube, video_data
from core.db.methods.create import create_chanel
from core.db.methods.request import get_channels_from_db
from core.db.methods.delete import delete_channel
from sqlalchemy.ext.asyncio import AsyncSession


from core.bot.utils.apsheduler import check_video_update

router = Router()


@router.message(Command(commands="check_video_update"))
async def get_video_update(message: Message, bot: Bot, session: AsyncSession):
    """Greetings"""
    await check_video_update(bot=bot, session=session)


@router.message(Command(commands="start"))
async def get_start(message: Message):
    """Greetings"""
    await message.answer(
        f"Привет {message.from_user.full_name}", reply_markup=get_main_menu()
    )


@router.message(Command(commands="channels"))
async def get_channels(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    channels = await get_channels_from_db(telegram_id=telegram_id, session=session)
    await message.answer(
        f"{message.from_user.full_name}, вот твои каналы:",
        reply_markup=get_channels_menu(channels),
    )


@router.callback_query(F.data.startswith("@"))
async def get_current_channel(callback: CallbackQuery):
    await callback.message.answer(
        text=f"{callback.data}", reply_markup=get_control_menu(callback.data)
    )
    await callback.answer()


@router.callback_query(F.data == "delete")
async def get_current_channel(callback: CallbackQuery):
    await callback.message.answer(
        text=f"{callback.data}", reply_markup=get_control_menu(callback.data)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("delete_"))
async def delete_current_channel(callback: CallbackQuery, session: AsyncSession):
    channel_id = callback.data.split("_", 1)[1]
    await delete_channel(channel_id=channel_id, session=session)
    await callback.message.answer(text=f"Канал {channel_id} успешно удален")
    await callback.answer()


class AddChannel(StatesGroup):
    added_channel_name = State()


@router.callback_query(F.data == "add_channel")
async def add_channel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите адрес канала в формате '@адресканала'",
    )
    await state.set_state(AddChannel.added_channel_name)
    await callback.answer()


@router.message(AddChannel.added_channel_name)
async def add_channel(message: Message, session: AsyncSession, state: FSMContext):
    telegram_id = message.from_user.id
    data = video_data(message.text)
    channel_name = data["channel_name"]
    last_video = data["id_last_video"]
    channel_id = data["channel_id"]
    await create_chanel(
        telegram_id=telegram_id,
        channel_id=channel_id,
        channel_name=channel_name,
        last_video=last_video,
        session=session,
    )
    await message.answer("Канал успешно добавлен")
    await state.clear()


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
    await message.answer(text="Неверный адрес, попробуйте еще раз")


@router.message(Command(commands="help"))
async def get_help(message: Message):
    """"""
    await message.answer(text="Помощь в разработке")


@router.message(Command(commands=["settings"]))
async def get_settings(message: Message):
    """"""
    await message.answer(text="Настройки в разработке")
