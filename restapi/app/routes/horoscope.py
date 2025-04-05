from datetime import date
from fastapi import APIRouter, Depends
from typing import Optional
from schemas import enums, responses
from services.horoscope import HoroscopeService
from schemas.requests import NatalChartRequest
from services.destiny_matrix import DestinyMatrixService
router = APIRouter(prefix="/horoscope", tags=["Horoscope"])

@router.get("/daily", response_model=responses.HoroscopeResponse)
async def get_daily_horoscope(
    zodiac_sign: enums.ZodiacSign,
    target_date: date = date.today(),
    service: HoroscopeService = Depends()
):
    return await service.get_daily_horoscope(zodiac_sign, target_date)

@router.get("/weekly", response_model=responses.HoroscopeResponse)
async def get_weekly_horoscope(
    zodiac_sign: enums.ZodiacSign,
    start_date: date = date.today(),
    service: HoroscopeService = Depends()
):
    return await service.get_weekly_horoscope(zodiac_sign, start_date)


@router.post("/natal", response_model=responses.NatalChartResponse)
async def get_natal_chart(
    chart_data: NatalChartRequest,
    service: HoroscopeService = Depends()
):
    return await service.get_natal_chart(
        birth_datetime=chart_data.birth_date,
        latitude=chart_data.latitude,
        longitude=chart_data.longitude
    )


@router.get("/destiny-matrix", response_model=responses.DestinyMatrixResponse)
async def get_destiny_matrix(
    birth_date: date,
    service: DestinyMatrixService = Depends()
):
    return await service.calculate_matrix(birth_date)