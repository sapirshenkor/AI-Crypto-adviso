from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "AI Crypto Advisor API"
    api_prefix: str = "/api"
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/ai_crypto_advisor"
    )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


settings = Settings()
