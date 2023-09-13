from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def get_channels_menu(channels: list) -> InlineKeyboardMarkup:
    """Keyboard to channels menu"""
    keyboard_builder = InlineKeyboardBuilder()
    for channel in channels:
        keyboard_builder.button(
            text=channel.channel_name,
            callback_data=f"channel_{channel.channel_name}_{channel.channel_id}",
        )
    keyboard_builder.button(text="Добавить 🪄", callback_data="add_channel")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_control_menu(channel_name: str, channel_id) -> InlineKeyboardMarkup:
    """Keyboard to delete a channel"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Перейти в канал",
        url=f"https://www.youtube.com/{channel_id}",
    )
    keyboard_builder.button(text="Удалить", callback_data=f"delete_{channel_name}")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_new_video_menu(url: str) -> InlineKeyboardMarkup:
    """Keyboard to convert updates"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Конвертировать в MP3", callback_data=f"convert_{url}")
    return keyboard_builder.as_markup()


def get_go_to_youtube_menu() -> InlineKeyboardMarkup:
    """Keyboard to convert updates"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Перейти в YouTube", url="https://www.youtube.com/")
    return keyboard_builder.as_markup()
