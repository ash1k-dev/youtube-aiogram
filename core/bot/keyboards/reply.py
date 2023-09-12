from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def get_main_menu() -> ReplyKeyboardMarkup:
    """Main keyboard"""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Мои каналы")
    keyboard_builder.button(text="Помощь")
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
