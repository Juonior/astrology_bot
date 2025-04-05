from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from messages import get_menu_text

def language_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
        ]
    ])
    return keyboard

def main_menu_keyboard(language='en'):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_menu_text('daily_horoscope', language))],
            [KeyboardButton(text=get_menu_text('weekly_horoscope', language))],
            [KeyboardButton(text=get_menu_text('fate_matrix', language))],
            [KeyboardButton(text=get_menu_text('natal_chart', language))],
            # [KeyboardButton(text=get_menu_text('change_birth_date', language))]
        ],
        resize_keyboard=True,
        input_field_placeholder=get_menu_text('menu', language)
    )
    return keyboard