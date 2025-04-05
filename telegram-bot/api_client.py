import httpx
import logging
from datetime import datetime
from dotenv import load_dotenv
import os
from typing import Optional, Dict, Any

load_dotenv()

logger = logging.getLogger(__name__)

class HoroscopeAPIClient:
    def __init__(self):
        self.base_url = os.getenv('HOROSCOPE_API_BASE_URL')
        self.client = httpx.AsyncClient(timeout=30.0)
        logger.info("Horoscope API client initialized")

    async def close(self):
        await self.client.aclose()
        logger.info("Horoscope API client closed")

    async def get_daily_horoscope(self, zodiac_sign: str, target_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            params = {"zodiac_sign": zodiac_sign}
            if target_date:
                params["target_date"] = target_date
            
            response = await self.client.get(
                f"{self.base_url}/horoscope/daily",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting daily horoscope: {e}")
            return None

    async def get_weekly_horoscope(self, zodiac_sign: str, start_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            params = {"zodiac_sign": zodiac_sign}
            if start_date:
                params["start_date"] = start_date
            
            response = await self.client.get(
                f"{self.base_url}/horoscope/weekly",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting weekly horoscope: {e}")
            return None

    async def get_natal_chart(self, birth_date: str, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        try:
            response = await self.client.post(
                f"{self.base_url}/horoscope/natal",
                json={
                    "birth_date": birth_date,
                    "latitude": latitude,
                    "longitude": longitude
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting natal chart: {e}")
            return None

    async def get_destiny_matrix(self, birth_date: datetime) -> Optional[Dict[str, Any]]:
        try:
            # Преобразуем datetime в строку в формате YYYY-MM-DD
            date_str = birth_date.strftime('%Y-%m-%d')
            response = await self.client.get(
                f"{self.base_url}/horoscope/destiny-matrix",
                params={"birth_date": date_str}  # Отправляем только дату без времени
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting destiny matrix: {e}")
            return None

api_client = HoroscopeAPIClient()