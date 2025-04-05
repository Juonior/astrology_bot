from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import config, exceptions
from routes import horoscope
import uvicorn

app = FastAPI(title=config.settings.app_name)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(
    exceptions.HoroscopeException,
    exceptions.horoscope_exception_handler
)

# Routes
app.include_router(horoscope.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.settings.app_host,
        port=config.settings.app_port,
        reload=config.settings.debug
    )