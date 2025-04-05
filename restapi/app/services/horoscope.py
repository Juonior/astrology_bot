from datetime import date
from typing import Dict, List, Optional
from schemas.enums import ZodiacSign
from core.exceptions import HoroscopeException
import datetime, random
from schemas.enums import ZodiacSign, Planet, House, AspectType

class HoroscopeService:
    def __init__(self):
        self._daily_data = {
            "aries": "Сегодня Овны почувствуют прилив энергии. Идеальный день для новых начинаний.",
            "taurus": "Тельцам стоит сосредоточиться на финансовых вопросах. Возможны неожиданные доходы.",
            "gemini": "Близнецы будут особенно общительны сегодня. Важные знакомства на горизонте.",
            "cancer": "Ракам нужно уделить время семье. Эмоциональный день, но продуктивный.",
            "leo": "Львы будут в центре внимания. Проявите свои творческие способности!",
            "virgo": "Девам стоит заняться анализом и планированием. День для работы, а не отдыха.",
            "libra": "Весам нужно искать баланс в отношениях. Избегайте конфликтов сегодня.",
            "scorpio": "Скорпионы придут к важным выводам. День глубоких размышлений.",
            "sagittarius": "Стрельцы могут планировать путешествия. Новые горизонты манят!",
            "capricorn": "Козерогам нужно сосредоточиться на карьере. Результаты будут заметны.",
            "aquarius": "Водолеи придумают инновационные решения. День для творчества.",
            "pisces": "Рыбам стоит довериться интуиции. Художественные занятия принесут успех."
        }
        
        self._weekly_data = {
            "aries": "На неделе Овнов ждёт много энергии, но будьте осторожны в среду - возможны конфликты.",
            "taurus": "Тельцам неделя принесёт стабильность, особенно в финансовой сфере. Четверг - лучший день.",
            "gemini": "Близнецы будут активно общаться всю неделю. В пятницу возможна важная встреча.",
            "cancer": "Ракам нужно беречь эмоции. Среда и пятница - самые напряжённые дни.",
            "leo": "Львов ждёт неделя признания. Особенно успешными будут вторник и суббота.",
            "virgo": "Девы смогут навести порядок во всех сферах. Понедельник - лучший день для планирования.",
            "libra": "Весы найдут баланс к середине недели. Избегайте поспешных решений в четверг.",
            "scorpio": "Скорпионов ждёт неделя трансформаций. Важные инсайты придут в среду.",
            "sagittarius": "Стрельцы могут начинать планировать путешествия. Выходные будут особенно удачны.",
            "capricorn": "Козероги добьются прогресса в карьере. Пятница - день важных решений.",
            "aquarius": "Водолеи придумают гениальные идеи. Записывайте мысли в среду утром.",
            "pisces": "Рыбы будут особенно интуитивны. Творческая энергия достигнет пика в четверг."
        }

        self._natal_data = {
            "planets": {
                "sun": "Солнце - ядро личности, жизненная энергия и сознание",
                "moon": "Луна - эмоции, подсознание, инстинкты",
                "mercury": "Меркурий - мышление, коммуникация, интеллект",
                "venus": "Венера - любовь, гармония, эстетика",
                "mars": "Марс - энергия, страсть, действия",
                "jupiter": "Юпитер - расширение, удача, рост",
                "saturn": "Сатурн - ограничения, дисциплина, карма",
                "uranus": "Уран - инновации, неожиданности, свобода",
                "neptune": "Нептун - интуиция, иллюзии, духовность",
                "pluto": "Плутон - трансформация, власть, возрождение",
                "ascendant": "Асцендент - внешнее проявление, первое впечатление",
                "midheaven": "Середина неба - карьера, призвание"
            },
            "houses": {
                "house1": "1 дом - Личность, внешность, самовыражение",
                "house2": "2 дом - Финансы, ценности, ресурсы",
                "house3": "3 дом - Коммуникация, обучение, ближайшее окружение",
                "house4": "4 дом - Дом, семья, корни",
                "house5": "5 дом - Творчество, любовь, дети",
                "house6": "6 дом - Работа, здоровье, рутина",
                "house7": "7 дом - Партнерство, брак, открытые враги",
                "house8": "8 дом - Секс, смерть, чужие ресурсы",
                "house9": "9 дом - Философия, путешествия, высшее образование",
                "house10": "10 дом - Карьера, репутация, социальный статус",
                "house11": "11 дом - Друзья, коллективы, надежды",
                "house12": "12 дом - Тайны, подсознание, изоляция"
            },
            "aspects": {
                "conjunction": "Соединение (0°) - сильное смешение энергий",
                "opposition": "Оппозиция (180°) - баланс противоположностей",
                "trine": "Трин (120°) - гармоничный поток энергии",
                "square": "Квадратура (90°) - напряжение и вызов",
                "sextile": "Секстиль (60°) - возможности и таланты",
                "quincunx": "Квиконс (150°) - необходимость адаптации",
                "semisextile": "Полусекстиль (30°) - слабая связь",
                "sesquisquare": "Сесквиквадрат (135°) - скрытое напряжение",
                "quintile": "Квинтиль (72°) - творческий потенциал",
                "biquintile": "Биквинтиль (144°) - скрытые таланты"
            },
            "sign_meanings": {
                "aries": "Овен - инициатива, смелость, импульсивность",
                "taurus": "Телец - стабильность, чувственность, упрямство",
                "gemini": "Близнецы - адаптивность, общительность, поверхностность",
                "cancer": "Рак - эмоциональность, забота, замкнутость",
                "leo": "Лев - творчество, гордость, тщеславие",
                "virgo": "Дева - анализ, практичность, критичность",
                "libra": "Весы - гармония, дипломатия, нерешительность",
                "scorpio": "Скорпион - страсть, глубина, манипуляции",
                "sagittarius": "Стрелец - свобода, оптимизм, прямолинейность",
                "capricorn": "Козерог - амбиции, дисциплина, холодность",
                "aquarius": "Водолей - оригинальность, дружелюбие, отстраненность",
                "pisces": "Рыбы - сострадание, интуиция, escapism"
            }
        }

    async def get_daily_horoscope(
        self, 
        zodiac_sign: ZodiacSign, 
        target_date: date = date.today()
    ) -> dict:
        if zodiac_sign.value not in self._daily_data:
            raise HoroscopeException(
                status_code=404,
                detail="Знак зодиака не найден"
            )
            
        return {
            "zodiac_sign": zodiac_sign.value,
            "date": target_date.isoformat(),
            "prediction": self._daily_data[zodiac_sign.value],
            "period": "day"
        }

    async def get_weekly_horoscope(
        self,
        zodiac_sign: ZodiacSign,
        start_date: date = date.today()
    ) -> dict:
        if zodiac_sign.value not in self._weekly_data:
            raise HoroscopeException(
                status_code=404,
                detail="Знак зодиака не найден"
            )
        
        end_date = date.fromordinal(start_date.toordinal() + 6)
        
        return {
            "zodiac_sign": zodiac_sign.value,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "prediction": self._weekly_data[zodiac_sign.value],
            "period": "week"
        }
    async def get_natal_chart(
        self,
        birth_datetime: datetime,
        latitude: float = 55.7558,
        longitude: float = 37.6173
    ) -> dict:
        """Основной метод получения натальной карты"""
        zodiac_sign = self._get_zodiac_sign(birth_datetime.date())
        planets = self._generate_planet_positions(birth_datetime)
        
        return {
            "zodiac_sign": zodiac_sign.value,
            "sign_meaning": self._natal_data["sign_meanings"][zodiac_sign.value],
            "birth_datetime": birth_datetime.isoformat(),
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "planets": planets,
            "houses": self._generate_houses(latitude, longitude, birth_datetime),
            "ascendant": self._calculate_ascendant(latitude, longitude, birth_datetime),
            "midheaven": self._calculate_midheaven(latitude, longitude, birth_datetime),
            "aspects": self._generate_aspects(planets)  # Теперь передаем планеты для расчета аспектов
        }
    

    def _get_zodiac_sign(self, birth_date: date) -> ZodiacSign:
        """Определяем знак зодиака по дате рождения"""
        day = birth_date.day
        month = birth_date.month
        
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return ZodiacSign.aries
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return ZodiacSign.taurus
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return ZodiacSign.gemini
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return ZodiacSign.cancer
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return ZodiacSign.leo
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return ZodiacSign.virgo
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return ZodiacSign.libra
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return ZodiacSign.scorpio
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return ZodiacSign.sagittarius
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return ZodiacSign.capricorn
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return ZodiacSign.aquarius
        else:
            return ZodiacSign.pisces

    def _generate_planet_positions(self, birth_datetime: datetime) -> List[Dict]:
        """Генерация позиций планет с заполненными значениями"""
        planet_meanings = {
            "sun": "Ядро личности, жизненная энергия",
            "moon": "Эмоции, подсознание, инстинкты",
            "mercury": "Мышление, коммуникация",
            "venus": "Любовь, гармония, ценности",
            "mars": "Энергия, действия, страсть",
            "jupiter": "Рост, удача, расширение",
            "saturn": "Ограничения, дисциплина, карма",
            "uranus": "Инновации, неожиданности",
            "neptune": "Интуиция, духовность",
            "pluto": "Трансформация, возрождение",
            "chiron": "Глубинные раны и исцеление",
            "north_node": "Кармическая задача развития",
            "south_node": "Кармический багаж прошлого",
            "ascendant": "Внешнее проявление личности",
            "midheaven": "Карьера, жизненные цели"
        }
        
        planets = []
        for planet in Planet:
            sign = random.choice(list(ZodiacSign))
            degree = random.randint(0, 29)
            house = random.randint(1, 12)
            
            planets.append({
                "planet": planet.value,
                "position": f"{degree}° {sign.value}",
                "house": house,
                "meaning": planet_meanings.get(planet.value, "Неизвестная планета")
            })
        
        return planets

    def _generate_houses(self, lat: float, lon: float, birth_datetime: datetime) -> List[Dict]:
        """Генерация домов гороскопа (заглушка)"""
        # В реальной реализации здесь должен быть расчет домов
        houses = []
        for house in House:
            houses.append({
                "house": house.value,
                "sign": random.choice(list(ZodiacSign)).value,
                "meaning": self._natal_data["houses"].get(house.value, "")
            })
        return houses

    def _calculate_ascendant(self, lat: float, lon: float, birth_datetime: datetime) -> Dict:
        """Расчет асцендента (заглушка)"""
        return {
            "sign": random.choice(list(ZodiacSign)).value,
            "degree": random.randint(0, 30),
            "meaning": "Асцендент показывает ваше внешнее 'я' и первое впечатление"
        }

    def _calculate_midheaven(self, lat: float, lon: float, birth_datetime: datetime) -> Dict:
        """Расчет середины неба (заглушка)"""
        return {
            "sign": random.choice(list(ZodiacSign)).value,
            "degree": random.randint(0, 30),
            "meaning": "Середина неба связана с карьерой и жизненными целями"
        }

    async def get_natal_chart(
        self,
        birth_datetime: datetime,
        latitude: float = 55.7558,
        longitude: float = 37.6173
    ) -> dict:
        """Основной метод получения натальной карты"""
        zodiac_sign = self._get_zodiac_sign(birth_datetime.date())
        planets = self._generate_planet_positions(birth_datetime)

        return {
            "zodiac_sign": zodiac_sign.value,
            "sign_meaning": self._natal_data["sign_meanings"][zodiac_sign.value],
            "birth_datetime": birth_datetime.isoformat(),
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "planets": self._generate_planet_positions(birth_datetime),
            "houses": self._generate_houses(latitude, longitude, birth_datetime),
            "ascendant": self._calculate_ascendant(latitude, longitude, birth_datetime),
            "midheaven": self._calculate_midheaven(latitude, longitude, birth_datetime),
            "aspects": self._generate_aspects(planets)
        }
    def _generate_aspects(self, planets: List[Dict]) -> List[Dict]:
        """Генерация аспектов между планетами"""
        aspects = []
        
        # Веса для разных аспектов (чем больше вес, тем чаще будет встречаться аспект)
        aspect_weights = {
            AspectType.conjunction: 3,
            AspectType.sextile: 3,
            AspectType.square: 2,
            AspectType.trine: 4,
            AspectType.opposition: 2,
            AspectType.semisextile: 1,
            AspectType.quincunx: 1,
            AspectType.quintile: 1,
            AspectType.biquintile: 1
        }
        
        main_planets = [p for p in planets if p['planet'] not in ['chiron', 'north_node', 'south_node']]
        
        for i in range(len(main_planets)):
            for j in range(i+1, len(main_planets)):
                aspect_type = random.choices(
                    list(aspect_weights.keys()),
                    weights=list(aspect_weights.values()),
                    k=1
                )[0]
                
                aspects.append({
                    "planet1": main_planets[i]['planet'],
                    "planet2": main_planets[j]['planet'],
                    "aspect_type": aspect_type.value,
                    "angle": self._get_aspect_angle(aspect_type),
                    "orb": round(random.uniform(0.1, 3.0), 1),
                    "meaning": self._natal_data["aspects"].get(aspect_type.value, "")
                })
        
        return aspects
    
    def _get_aspect_angle(self, aspect_type: AspectType) -> int:
        """Возвращает стандартный угол для аспекта"""
        angles = {
            AspectType.conjunction: 0,
            AspectType.sextile: 60,
            AspectType.square: 90,
            AspectType.trine: 120,
            AspectType.opposition: 180,
            AspectType.semisextile: 30,
            AspectType.quincunx: 150,
            AspectType.quintile: 72,
            AspectType.biquintile: 144
        }
        return angles.get(aspect_type, 0)