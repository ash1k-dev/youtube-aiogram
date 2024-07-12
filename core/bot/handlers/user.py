from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import HELP_TEXT
from core.bot.keyboards.inline import (get_channels_menu, get_control_menu,
                                       get_go_to_youtube_menu)
from core.bot.keyboards.reply import get_main_menu
from core.db.methods.create import create_chanel, create_user
from core.db.methods.delete import delete_channel
from core.db.methods.request import (check_channel_in_db,
                                     get_all_channels_from_db,
                                     get_user_from_db)
from core.youtube.services import (delete_saved_mp3, get_mp3_from_youtube,
                                   get_video_data)

router = Router()


@router.message(Command(commands="start"))
async def get_start(message: Message, session: AsyncSession):
    """Welcome and registration a new user"""
    telegram_id = message.from_user.id
    result = await get_user_from_db(telegram_id=telegram_id, session=session)
    if result is None:
        await create_user(
            user_name=message.from_user.full_name,
            telegram_id=telegram_id,
            session=session,
        )
    await message.answer(
        f"Привет {message.from_user.full_name}", reply_markup=get_main_menu()
    )


@router.message(F.text == "Мои каналы")
async def get_channels(message: Message, session: AsyncSession):
    """Show user channels"""
    telegram_id = message.from_user.id
    channels = await get_all_channels_from_db(telegram_id=telegram_id, session=session)
    await message.answer(
        f"{message.from_user.full_name}, вот твои каналы:",
        reply_markup=get_channels_menu(channels),
    )


@router.message(F.text == "Помощь")
async def get_help(message: Message):
    """Show help text"""
    await message.answer(text=HELP_TEXT)


@router.message(F.text == "YouTube")
async def go_to_youtube(message: Message):
    """Show help text"""
    await message.answer(
        text="Перейти на YouTube", reply_markup=get_go_to_youtube_menu()
    )


@router.callback_query(F.data.startswith("channel_"))
async def get_current_channel(callback: CallbackQuery):
    """Show current channel and keyboard"""
    channel_name = callback.data.split("_")[1]
    channel_id = callback.data.split("_")[2]
    await callback.message.answer(
        text=f"{channel_name}", reply_markup=get_control_menu(channel_name, channel_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("delete_"))
async def delete_current_channel(callback: CallbackQuery, session: AsyncSession):
    """Show current channel and delete keyboard"""
    channel_name = callback.data.split("_", 1)[1]
    await delete_channel(channel_name=channel_name, session=session)
    await callback.message.delete()
    await callback.message.answer(text=f"Канал '{channel_name}' успешно удален")
    await callback.answer()


@router.callback_query(
    F.data.startswith("convert_"), flags={"long_operation": "upload_document"}
)
async def convert_new_video(callback: CallbackQuery, bot: Bot):
    """New video conversion"""
    new_video_url = callback.data.split("_", 1)[1]
    try:
        audio = get_mp3_from_youtube(new_video_url)
        await bot.send_audio(callback.from_user.id, audio=audio)
        delete_saved_mp3(audio.__dict__["path"])
    except Exception:
        await bot.send_message(callback.from_user.id, text="Сбой, попробуйте еще раз!")
    await callback.answer()


class AddChannel(StatesGroup):
    """State to add channel"""

    added_channel_name = State()


@router.callback_query(F.data == "add_channel")
async def add_channel(callback: CallbackQuery, state: FSMContext):
    """Channel adding stage"""
    await callback.message.answer(
        text="Введите адрес канала:",
    )
    await state.set_state(AddChannel.added_channel_name)
    await callback.answer()


@router.message(AddChannel.added_channel_name)
async def add_channel(message: Message, session: AsyncSession, state: FSMContext):
    """Adding a channel"""
    try:
        data = get_video_data(message.text)
    except Exception:
        await message.answer(text=f"Некорректный адрес канала, попробуйте еще раз")
    else:
        channel = await check_channel_in_db(
            channel_url=message.text, telegram_id=message.from_user.id, session=session
        )
        if channel is not None:
            await message.answer(text="Этот канал уже в вашем списке")
        else:
            channel_name = data["channel_name"]
            last_video = data["id_last_video"]
            channel_id = data["channel_id"]
            telegram_id = message.from_user.id
            await create_chanel(
                telegram_id=telegram_id,
                channel_id=channel_id,
                channel_name=channel_name,
                last_video=last_video,
                session=session,
            )
            await message.answer(f"Канал '{channel_name}' успешно добавлен")
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
            message.chat.id, text=f"Неверный адрес, попробуйте еще раз"
        )
