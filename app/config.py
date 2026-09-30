"""Настройки приложения (аналог appsettings.json)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Аналог ConnectionStrings:DefaultConnection
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/timescale_db"
    log_level: str = "INFO"


settings = Settings()
