from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def get_channels_menu(channels: list) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    for channel in channels:
        keyboard_builder.button(
            text=channel.channel_name, callback_data=channel.channel_id
        )
    keyboard_builder.button(text="Добавить", callback_data="add_channel")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_control_menu(data) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Удалить", callback_data=f"delete_{data}")
    keyboard_builder.button(text="Назад", callback_data="channels")
    return keyboard_builder.as_markup()
