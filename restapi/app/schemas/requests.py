from pydantic import BaseModel
from datetime import datetime

class DestinyMatrixRequest(BaseModel):
    birth_date: datetime
    
class NatalChartRequest(BaseModel):
    birth_date: datetime  # Теперь принимает дату и время
    latitude: float = 55.7558  # Широта по умолчанию (Москва)
    longitude: float = 37.6173  # Долгота по умолчанию (Москва)