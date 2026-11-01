import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "KisanShield"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/backend/kisanshield.db"
    
    # LLM Settings
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # External API Timeouts & Cache TTL
    API_TIMEOUT_SECONDS: int = 5
    WEATHER_CACHE_TTL_MINUTES: int = 60
    MANDI_CACHE_TTL_MINUTES: int = 120
    
    # Data paths
    DATA_DIR: Path = BASE_DIR / "data"
    KNOWLEDGE_BASE_DIR: Path = BASE_DIR / "data" / "knowledge_base"
    SEED_DATA_DIR: Path = BASE_DIR / "data" / "seed_data"
    MANDI_SAMPLES_DIR: Path = BASE_DIR / "data" / "mandi_samples"
    ENSO_DIR: Path = BASE_DIR / "data" / "enso"

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()

