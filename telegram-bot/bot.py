import os
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, 
    CallbackQuery, 
    ReplyKeyboardRemove,
    Location
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
import dateparser
from typing import Optional

from database import db
from keyboards import language_keyboard, main_menu_keyboard
from messages import get_message, get_menu_text
from logger import logger
from api_client import api_client

load_dotenv()

class Form(StatesGroup):
    language = State()
    birth_date = State()
    natal_location = State()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

async def startup():
    logger.info("Starting bot...")
    await db.connect()
    await api_client.client.__aenter__()

async def shutdown():
    logger.info("Shutting down bot...")
    await db.close()
    await api_client.client.__aexit__(None, None, None)

async def show_main_menu(user_id: int, language: str, message=None, edit=False):
    text = get_message('welcome_back', language)
    keyboard = main_menu_keyboard(language)
    
    if message and edit:
        await message.edit_text(text, reply_markup=keyboard)
    elif message:
        await message.answer(text, reply_markup=keyboard)
    else:
        await bot.send_message(user_id, text, reply_markup=keyboard)

async def get_zodiac_sign(birth_date: datetime) -> str:
    # Simple zodiac sign calculation based on date
    day = birth_date.day
    month = birth_date.month
    
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "aquarius"
    else:
        return "pisces"

@dp.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started the bot")
    user = await db.get_user(message.from_user.id)
    
    # Если пользователь есть в БД И у него указан язык
    if user and user['language']:
        logger.info(f"Registered user {message.from_user.id} returned")
        # Если есть дата рождения - показываем меню
        if user['birth_date']:
            await show_main_menu(message.from_user.id, user['language'], message)
        else:
            # Если нет даты - просим ввести
            await state.set_state(Form.birth_date)
            await message.answer(get_message('enter_birth_date', user['language']))
        await state.clear()
    else:
        logger.info(f"New user {message.from_user.id} detected")
        await db.create_user(message.from_user.id)
        await state.set_state(Form.language)
        await message.answer(
            get_message('start'),
            reply_markup=language_keyboard()
        )

@dp.callback_query(F.data.startswith('lang_'), Form.language)
async def process_language(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    language = callback.data.split('_')[1]
    
    logger.info(f"User {user_id} selected language: {language}")
    
    try:
        # Обновляем язык пользователя
        await db.update_user_language(user_id, language)
        
        # Переводим в состояние ввода даты рождения
        await state.set_state(Form.birth_date)
        
        # Редактируем сообщение с кнопками выбора языка
        await callback.message.edit_text(
            get_message('enter_birth_date', language)
        )
        
        # Подтверждаем обработку callback
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error processing language for user {user_id}: {e}")
        await callback.answer(
            "⚠️ Произошла ошибка. Пожалуйста, попробуйте еще раз.",
            show_alert=True
        )

@dp.message(Form.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()
    
    logger.info(f"User {user_id} entered birth date: {text}")
    
    # Получаем данные пользователя
    user = await db.get_user(user_id)
    if not user:
        logger.warning(f"User {user_id} not found in database")
        return
    
    try:
        # Парсим дату рождения
        birth_date = dateparser.parse(text, date_formats=['%d.%m.%Y %H:%M'])
        if not birth_date:
            raise ValueError("Invalid date format")
        
        # Обновляем дату рождения в БД
        await db.update_user_birth_date(user_id, birth_date)
        logger.info(f"Birth date saved for user {user_id}: {birth_date}")
        
        # Отправляем подтверждение
        await message.answer(
            get_message('birth_date_saved', user['language'])
        )
        
        # Показываем главное меню
        await show_main_menu(user_id, user['language'], message)
        
        # Очищаем состояние
        await state.clear()
        
    except (ValueError, AttributeError) as e:
        logger.warning(f"Invalid date from user {user_id}: {text}. Error: {e}")
        await message.answer(
            get_message('invalid_date', user['language'])
        )
    except Exception as e:
        logger.error(f"Error processing birth date for user {user_id}: {e}")
        await message.answer(
            "⚠️ Произошла ошибка. Пожалуйста, попробуйте позже."
        )

@dp.message(F.text == get_menu_text('daily_horoscope', 'ru'))
@dp.message(F.text == get_menu_text('daily_horoscope', 'en'))
async def handle_daily_horoscope(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user or not user['birth_date']:
        return
    
    logger.info(f"User {message.from_user.id} requested daily horoscope")
    zodiac_sign = await get_zodiac_sign(user['birth_date'])
    
    await message.answer(get_message('calculating', user['language']))
    
    horoscope = await api_client.get_daily_horoscope(
        zodiac_sign=zodiac_sign,
        target_date=datetime.now().strftime('%Y-%m-%d')
    )
    
    if horoscope:
        response_text = (
            f"{get_message('daily_horoscope', user['language'])}\n\n"
            f"{horoscope.get('prediction', 'No prediction available')}"
        )
        await message.answer(response_text)
    else:
        await message.answer(get_message('api_error', user['language']))

@dp.message(F.text == get_menu_text('weekly_horoscope', 'ru'))
@dp.message(F.text == get_menu_text('weekly_horoscope', 'en'))
async def handle_weekly_horoscope(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user or not user['birth_date']:
        return
    
    logger.info(f"User {message.from_user.id} requested weekly horoscope")
    zodiac_sign = await get_zodiac_sign(user['birth_date'])
    
    await message.answer(get_message('calculating', user['language']))
    
    horoscope = await api_client.get_weekly_horoscope(
        zodiac_sign=zodiac_sign,
        start_date=datetime.now().strftime('%Y-%m-%d')
    )
    
    if horoscope:
        response_text = (
            f"{get_message('weekly_horoscope', user['language'])}\n\n"
            f"{horoscope.get('prediction', 'No prediction available')}\n\n"
            f"📅 {horoscope.get('start_date', '')} - {horoscope.get('end_date', '')}"
        )
        await message.answer(response_text)
    else:
        await message.answer(get_message('api_error', user['language']))

@dp.message(F.text == get_menu_text('natal_chart', 'ru'))
@dp.message(F.text == get_menu_text('natal_chart', 'en'))
async def handle_natal_chart_request(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user or not user['birth_date']:
        return
    
    logger.info(f"User {message.from_user.id} requested natal chart")
    await state.set_state(Form.natal_location)
    await message.answer(
        get_message('request_location', user['language']),
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(Form.natal_location, F.location)
async def handle_location(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user or not user['birth_date']:
        return
    
    location = message.location
    logger.info(f"User {message.from_user.id} shared location: {location.latitude}, {location.longitude}")
    
    lang = user['language']
    await message.answer(get_message('location_received', lang))
    await message.answer(get_message('calculating', lang))
    
    natal_chart = await api_client.get_natal_chart(
        birth_date=user['birth_date'].isoformat(),
        latitude=location.latitude,
        longitude=location.longitude
    )
    
    if not natal_chart:
        await message.answer(get_message('api_error', lang))
        await state.clear()
        return
    
    # Основная информация
    response_parts = [
        f"🌌 *{get_message('natal_chart', lang)}* 🌌\n",
        f"♈ {get_zodiac_sign_emoji(natal_chart['zodiac_sign'])} "
        f"{get_localized('zodiac_sign', natal_chart['zodiac_sign'], lang)}: "
        f"{natal_chart.get('sign_meaning', 'N/A')}\n",
        f"📅 {get_localized('birth_date', None, lang)}: "
        f"{format_datetime(natal_chart['birth_datetime'], lang)}\n",
        f"📍 {get_localized('coordinates', None, lang)}: "
        f"{natal_chart['coordinates']['latitude']:.4f}, "
        f"{natal_chart['coordinates']['longitude']:.4f}\n"
    ]

    # Асцендент и MC
    asc = natal_chart.get('ascendant', {})
    mc = natal_chart.get('midheaven', {})
    response_parts.extend([
        f"\n🌞 *{get_localized('ascendant', None, lang)}*: ",
        f"{asc.get('sign', 'N/A')} {asc.get('degree', 0)}°\n",
        f"_{asc.get('meaning', '')}_\n",
        f"🌙 *{get_localized('midheaven', None, lang)}*: ",
        f"{mc.get('sign', 'N/A')} {mc.get('degree', 0)}°\n",
        f"_{mc.get('meaning', '')}_\n"
    ])

    # Планеты
    response_parts.append(f"\n🪐 *{get_localized('planets', None, lang)}*:\n")
    for planet in natal_chart.get('planets', [])[:5]:  # Первые 5 для примера
        response_parts.append(
            f"{get_planet_emoji(planet['planet'])} "
            f"{get_localized(planet['planet'], None, lang)}: "
            f"{planet['position']} ({get_localized('house', None, lang)} {planet['house']})\n"
            f"_{planet['meaning']}_\n\n"
        )

    # Дома
    response_parts.append(f"\n🏠 *{get_localized('houses', None, lang)}*:\n")
    for house in natal_chart.get('houses', [])[:4]:  # Первые 4 для примера
        response_parts.append(
            f"{get_house_emoji(house['house'])} "
            f"{house['house'].replace('house', '')} {get_localized('house', None, lang)}: "
            f"{house['sign']}\n"
            f"_{house['meaning']}_\n\n"
        )

    # Аспекты (только основные)
    response_parts.append(f"\n🔮 *{get_localized('main_aspects', None, lang)}*:\n")
    for aspect in natal_chart.get('aspects', [])[:3]:  # Первые 3 для примера
        response_parts.append(
            f"{get_aspect_emoji(aspect['aspect_type'])} "
            f"{get_localized(aspect['planet1'], None, lang)} → "
            f"{get_localized(aspect['planet2'], None, lang)}: "
            f"{get_localized(aspect['aspect_type'], None, lang)} "
            f"({aspect['angle']}°)\n"
            f"_{aspect['meaning']}_\n\n"
        )

    # Разбиваем сообщение на части, если оно слишком длинное
    full_text = ''.join(response_parts)
    for part in split_message(full_text, 4096):
        await message.answer(part, parse_mode="Markdown")
    
    await state.clear()
    await show_main_menu(message.from_user.id, lang, message)

# Вспомогательные функции
def get_localized(key: str, value: Optional[str] = None, lang: str = 'en') -> str:
    """Локализация текста"""
    localized = {
        'zodiac_sign': {
            'ru': {'aries': 'Овен', 'taurus': 'Телец', 'gemini': 'Близнецы'},
            'en': {'aries': 'Aries', 'taurus': 'Taurus', 'gemini': 'Gemini'}
        },
        'birth_date': {'ru': 'Дата рождения', 'en': 'Birth date'},
        'coordinates': {'ru': 'Координаты', 'en': 'Coordinates'},
        'ascendant': {'ru': 'Асцендент', 'en': 'Ascendant'},
        'midheaven': {'ru': 'Середина неба', 'en': 'Midheaven'},
        'planets': {'ru': 'Планеты', 'en': 'Planets'},
        'houses': {'ru': 'Дома', 'en': 'Houses'},
        'main_aspects': {'ru': 'Основные аспекты', 'en': 'Main aspects'},
        'house': {'ru': 'дом', 'en': 'house'},
        # Добавьте другие ключи по аналогии
    }
    
    if value and key in localized:
        return localized[key][lang].get(value, value)
    return localized.get(key, {}).get(lang, key)

def get_zodiac_sign_emoji(sign: str) -> str:
    """Возвращает emoji для знака зодиака"""
    emoji_map = {
        'aries': '♈', 'taurus': '♉', 'gemini': '♊',
        'cancer': '♋', 'leo': '♌', 'virgo': '♍',
        'libra': '♎', 'scorpio': '♏', 'sagittarius': '♐',
        'capricorn': '♑', 'aquarius': '♒', 'pisces': '♓'
    }
    return emoji_map.get(sign.lower(), '✨')

def get_planet_emoji(planet: str) -> str:
    """Возвращает emoji для планеты"""
    emoji_map = {
        'sun': '☀️', 'moon': '🌙', 'mercury': '☿',
        'venus': '♀️', 'mars': '♂️', 'jupiter': '♃',
        'saturn': '♄', 'uranus': '♅', 'neptune': '♆',
        'pluto': '♇', 'ascendant': '🔼', 'midheaven': '⏫'
    }
    return emoji_map.get(planet.lower(), '🪐')

def get_house_emoji(house: str) -> str:
    """Возвращает emoji для дома"""
    house_num = house.replace('house', '')
    return f'{house_num}️⃣' if house_num.isdigit() else '🏠'

def get_aspect_emoji(aspect_type: str) -> str:
    """Возвращает emoji для аспекта"""
    emoji_map = {
        'conjunction': '⚡', 'opposition': '⚖️',
        'trine': '△', 'square': '□',
        'sextile': '⚹', 'quincunx': '⚻'
    }
    return emoji_map.get(aspect_type.lower(), '🔹')

def format_datetime(dt_str: str, lang: str) -> str:
    """Форматирование даты"""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        if lang == 'ru':
            return dt.strftime('%d.%m.%Y %H:%M')
        return dt.strftime('%m/%d/%Y %I:%M %p')
    except:
        return dt_str

def split_message(text: str, max_len: int) -> list[str]:
    """Разбивает длинное сообщение на части"""
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]

@dp.message(F.text == get_menu_text('fate_matrix', 'ru'))
@dp.message(F.text == get_menu_text('fate_matrix', 'en'))
async def handle_fate_matrix(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user or not user['birth_date']:
        return
    
    logger.info(f"User {message.from_user.id} requested fate matrix")
    await message.answer(get_message('calculating', user['language']))
    
    # Передаем datetime объект, а не строку
    fate_matrix = await api_client.get_destiny_matrix(
        birth_date=user['birth_date']  # Уже datetime из базы данных
    )
    
    if fate_matrix:
        response_text = (
            f"{get_message('fate_matrix', user['language'])}\n\n"
            f"📅 Дата рождения: {fate_matrix.get('birth_date', 'N/A')}\n"
            f"🔢 Число судьбы: {fate_matrix.get('destiny_number', 'N/A')}\n"
            f"👤 Число личности: {fate_matrix.get('personality_number', 'N/A')}\n"
            f"🛤️ Число жизненного пути: {fate_matrix.get('life_path_number', 'N/A')}\n\n"
            f"🧮 Матрица:\n"
        )
        
        # Add matrix visualization
        matrix = fate_matrix.get('matrix', [])
        for row in matrix:
            response_text += ' '.join(str(num) for num in row) + '\n'
        
        response_text += f"\n📖 Интерпретация:\n{fate_matrix.get('interpretation', 'N/A')}"
        
        await message.answer(response_text)
    else:
        await message.answer(get_message('api_error', user['language']))

# Previous change_birth_date handler remains the same

async def main():
    await startup()
    await dp.start_polling(bot)
    await shutdown()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())