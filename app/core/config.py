from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Expedia Inspired API"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database Settings
    DB_URL: str = "sqlite:///./expedia_inspired.db"
    
    # JWT Settings
    JWT_SECRET: str = "jwt_secret_change_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OTP & Email Settings
    DEVELOPMENT_MODE: bool = True
    STATIC_OTP: str = "123456"
    OTP_EXPIRY_MINUTES: int = 10
    
    # Email Settings (for Production)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = "noreply@expedia-inspired.com"

    class Config:
        env_file = ".env"

settings = Settings()

def print_startup_config():
    print("\n" + "="*60)
    print(f"🚀 {settings.APP_NAME} v{settings.VERSION}")
    print("="*60)
    print(f"🔧 Environment: {'Development' if settings.DEVELOPMENT_MODE else 'Production'}")
    print(f"📧 OTP System: {'Static OTP (' + settings.STATIC_OTP + ')' if settings.DEVELOPMENT_MODE else 'Email Integration'}")
    print(f"⏰ OTP Expiry: {settings.OTP_EXPIRY_MINUTES} minutes")
    print(f"🗄️  Database: {settings.DB_URL}")
    print("="*60 + "\n")