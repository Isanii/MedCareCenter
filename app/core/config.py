from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "MedCare API"
    APP_VERSION: str = "2.0.0"

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env"
    )
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str

    MAIL_SERVER: str
    MAIL_PORT: int

    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

@lru_cache
def get_settings():
    return Settings()


settings = get_settings()