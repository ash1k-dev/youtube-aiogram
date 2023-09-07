from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def get_channels_menu(channels: list) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    for channel in channels:
        keyboard_builder.button(
            text=channel.channel_name, callback_data=f"channel_{channel.channel_name}"
        )
    keyboard_builder.button(text="Добавить 🪄", callback_data="add_channel")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_control_menu(data: str) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Удалить", callback_data=f"delete_{data}")
    return keyboard_builder.as_markup()


def get_new_video_menu(url: str) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Конвертировать в MP3", callback_data=f"convert_{url}")
    return keyboard_builder.as_markup()
