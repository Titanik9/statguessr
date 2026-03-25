from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    public_base_url: str = "http://localhost:3000"
    database_url: str = "sqlite:///./relay_console.db"
    redis_url: str = "redis://localhost:6379/0"
    clickhouse_url: str = "http://localhost:8123"
    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "relay-console"
    jwt_secret: str = Field(default="change-me-with-at-least-32-characters", min_length=32)
    encryption_key: str = Field(default="change-me-32-bytes-minimum", min_length=16)
    magic_link_ttl_minutes: int = 15
    session_ttl_hours: int = 24 * 7
    mail_from: str = "hello@relay-console.local"
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    auth_dev_preview: bool = True
    auto_migrate_on_boot: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
