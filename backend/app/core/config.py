from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = ROOT_DIR / ".env"


BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "AI Crypto Advisor API"
    api_prefix: str = "/api"
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/ai_crypto_advisor"
    )
    jwt_secret_key: str = "change-this-secret-in-development"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    news_data_api_key: str = ""
    coingecko_demo_api_key: str = ""
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-oss-120b:free"
    openrouter_fallback_model: str = "google/gemma-4-26b-a4b-it:free"
    coingecko_api_base_url: str = "https://api.coingecko.com/api/v3"
    news_data_api_base_url: str = "https://newsdata.io/api/1"
    openrouter_api_base_url: str = "https://openrouter.ai/api/v1"
    backend_public_url: str = "http://localhost:8000"
    external_api_timeout_seconds: int = 8

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


settings = Settings()
