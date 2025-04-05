from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class HoroscopeException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

async def horoscope_exception_handler(request: Request, exc: HoroscopeException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )