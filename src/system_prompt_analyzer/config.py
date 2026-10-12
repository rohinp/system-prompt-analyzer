from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "System Prompt Analyzer"
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8001
    model_provider: str = "openai"
    model_name: str = "gpt-5-mini"
    model_api_key: str | None = None
    model_base_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
