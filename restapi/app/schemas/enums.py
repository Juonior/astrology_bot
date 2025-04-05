from enum import Enum

class ZodiacSign(str, Enum):
    aries = "aries"
    taurus = "taurus"
    gemini = "gemini"
    cancer = "cancer"
    leo = "leo"
    virgo = "virgo"
    libra = "libra"
    scorpio = "scorpio"
    sagittarius = "sagittarius"
    capricorn = "capricorn"
    aquarius = "aquarius"
    pisces = "pisces"

class Planet(str, Enum):
    sun = "sun"
    moon = "moon"
    mercury = "mercury"
    venus = "venus"
    mars = "mars"
    jupiter = "jupiter"
    saturn = "saturn"
    uranus = "uranus"
    neptune = "neptune"
    pluto = "pluto"
    chiron = "chiron"
    north_node = "north_node"
    south_node = "south_node"
    ascendant = "ascendant"
    midheaven = "midheaven"

class House(str, Enum):
    house1 = "house1"
    house2 = "house2"
    house3 = "house3"
    house4 = "house4"
    house5 = "house5"
    house6 = "house6"
    house7 = "house7"
    house8 = "house8"
    house9 = "house9"
    house10 = "house10"
    house11 = "house11"
    house12 = "house12"

class AspectType(str, Enum):
    conjunction = "conjunction"        # 0°
    sextile = "sextile"                # 60°
    square = "square"                  # 90°
    trine = "trine"                    # 120°
    opposition = "opposition"          # 180°
    # Дополнительные аспекты:
    semisextile = "semisextile"        # 30°
    quincunx = "quincunx"              # 150°
    quintile = "quintile"              # 72°
    biquintile = "biquintile"          # 144°
    # Удаляем sesquisquare, так как он редко используется

class ChartType(str, Enum):
    natal = "natal"
    solar = "solar"
    lunar = "lunar"
    synastry = "synastry"
    transit = "transit"