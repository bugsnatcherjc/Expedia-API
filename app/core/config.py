from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "expedia_inspired"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    JWT_SECRET: str = "jwt_secret"
    DB_URL: str = "sqlite+aiosqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()