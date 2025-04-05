MESSAGES = {
    'start': {
        'ru': '✨ Добро пожаловать! Выберите язык:',
        'en': '✨ Welcome! Choose language:'
    },
    'enter_birth_date': {
        'ru': '📅 Пожалуйста, введите свою дату рождения и время в формате ДД.ММ.ГГГГ ЧЧ:ММ\n\nПример: 15.05.1990 14:30',
        'en': '📅 Please enter your birth date and time in format DD.MM.YYYY HH:MM\n\nExample: 15.05.1990 14:30'
    },
    'birth_date_saved': {
        'ru': '✅ Ваша дата рождения сохранена!',
        'en': '✅ Your birth date has been saved!'
    },
    'invalid_date': {
        'ru': '❌ Неверный формат даты. Пожалуйста, используйте ДД.ММ.ГГГГ ЧЧ:ММ\n\nПример: 15.05.1990 14:30',
        'en': '❌ Invalid date format. Please use DD.MM.YYYY HH:MM\n\nExample: 15.05.1990 14:30'
    },
    'welcome_back': {
        'ru': '👋 С возвращением! Вот ваше меню:',
        'en': '👋 Welcome back! Here is your menu:'
    },
    'menu': {
        'ru': '📜 Главное меню:',
        'en': '📜 Main menu:'
    },
    'daily_horoscope': {
        'ru': '🔮 Ваш гороскоп на сегодня:',
        'en': '🔮 Your daily horoscope:'
    },
    'weekly_horoscope': {
        'ru': '📆 Ваш гороскоп на неделю:',
        'en': '📆 Your weekly horoscope:'
    },
    'fate_matrix': {
        'ru': '🧮 Ваша матрица судьбы:',
        'en': '🧮 Your fate matrix:'
    },
    'natal_chart': {
        'ru': '🌌 Ваша натальная карта:',
        'en': '🌌 Your natal chart:'
    },
    'request_location': {
        'ru': '📍 Пожалуйста, отправьте ваше местоположение для точного расчета натальной карты:',
        'en': '📍 Please share your location for accurate natal chart calculation:'
    },
    'location_received': {
        'ru': '✅ Местоположение получено! Рассчитываю вашу натальную карту...',
        'en': '✅ Location received! Calculating your natal chart...'
    },
    'calculating': {
        'ru': '⏳ Рассчитываю...',
        'en': '⏳ Calculating...'
    },
    'api_error': {
        'ru': '❌ Произошла ошибка при получении данных. Пожалуйста, попробуйте позже.',
        'en': '❌ An error occurred while fetching data. Please try again later.'
    }
}

MENU_ITEMS = {
    'daily_horoscope': {
        'ru': '🔮 Гороскоп на сегодня',
        'en': '🔮 Daily horoscope'
    },
    'weekly_horoscope': {
        'ru': '📆 Гороскоп на неделю',
        'en': '📆 Weekly horoscope'
    },
    'fate_matrix': {
        'ru': '🧮 Матрица судьбы',
        'en': '🧮 Fate matrix'
    },
    'natal_chart': {
        'ru': '🌌 Натальная карта',
        'en': '🌌 Natal chart'
    },
    'change_birth_date': {
        'ru': '🔄 Изменить дату рождения',
        'en': '🔄 Change birth date'
    }
}

def get_message(key, language='en'):
    return MESSAGES.get(key, {}).get(language, '')

def get_menu_text(key, language='en'):
    return MENU_ITEMS.get(key, {}).get(language, '')