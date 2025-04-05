from pydantic_settings import BaseSettings

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Horoscope API"
    debug: bool = False
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
