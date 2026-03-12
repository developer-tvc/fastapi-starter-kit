from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    DESCRIPTION: str
    DEBUG: bool
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    SWAGGER_LOGIN: str | None = None
    SMTP_SERVER:str
    SMTP_PORT:int
    SMTP_USERNAME:str
    SMTP_PASSWORD:str
    EMAIL_VERIFICATION_ENABLED: bool
    LOGIN_MAX_ATTEMPTS:int
    LOGIN_LOCK_ENABLED:bool
    LOGIN_LOCK_MINUTES:int
    EMAIL_NOTIFICATION_ENABLED: bool
    SMS_NOTIFICATION_ENABLED: bool
    WEBHOOK_NOTIFICATION_ENABLED: bool
    IN_APP_NOTIFICATION_ENABLED: bool
    SMS_PROVIDER: str = "mock"
    SMS_API_KEY: str | None = None
    SMS_SENDER_ID: str = "MyApp"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> "Settings":
    return Settings()


settings = get_settings()