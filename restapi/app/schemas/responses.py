from datetime import date
from typing import Optional, List, Dict
from pydantic import BaseModel

class HoroscopeResponse(BaseModel):
    zodiac_sign: str
    date: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    prediction: str
    period: str

class PlanetPosition(BaseModel):
    planet: str
    position: str
    house: int
    meaning: str

class HouseInfo(BaseModel):
    house: str
    sign: str
    meaning: str

class AnglePoint(BaseModel):
    sign: str
    degree: int
    meaning: str

class NatalChartResponse(BaseModel):
    zodiac_sign: str
    sign_meaning: str
    birth_datetime: str
    coordinates: dict
    planets: List[PlanetPosition]
    houses: List[HouseInfo]
    ascendant: AnglePoint
    midheaven: AnglePoint
    aspects: List[dict]

class DestinyMatrixResponse(BaseModel):
    birth_date: str
    energy_centers: Dict[str, int]
    money_line: List[int]
    family_line: List[int]
    health_line: List[int]
    talents_line: List[int]
    destiny_number: int
    personality_number: int
    life_path_number: int
    matrix: List[List[int]]
    interpretation: str