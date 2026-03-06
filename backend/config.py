"""
NBA Props App - Yapılandırma Modülü

Tüm ortam değişkenlerini tek bir yerden yönetir.
Pydantic Settings kullanarak .env dosyasından otomatik okur.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Uygulama ayarları — .env dosyasından otomatik yüklenir."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Veritabanı ---
    DATABASE_URL: str = "postgresql+asyncpg://nbaprops:nbaprops_secret_2026@localhost:5432/nba_props_db"

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- API Anahtarları ---
    BALLDONTLIE_API_KEY: str = ""
    ODDS_API_KEY: str = ""

    # --- Telegram ---
    TELEGRAM_BOT_TOKEN: str = ""

    # --- Uygulama ---
    APP_ENV: str = "development"
    APP_DEBUG: bool = True

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


# Tek bir settings nesnesi oluştur — tüm modüller bunu import eder
settings = Settings()
