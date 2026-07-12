from functools import lru_cache

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: PostgresDsn
    secret_key: str = Field(min_length=32)
    access_token_expire_minutes: int = Field(default=30, gt=0, le=1440)
    db_ssl_required: bool = False
    environment: str = "development"

    @field_validator("secret_key")
    @classmethod
    def reject_example_secret(cls, value: str) -> str:
        if "change-me" in value.lower():
            raise ValueError("SECRET_KEY must be replaced with a securely generated value")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
